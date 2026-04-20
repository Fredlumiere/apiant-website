import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";
import { hashPasswordBcrypt, isBcryptHash, verifyPassword } from "../_shared/auth.ts";
import { verifyTurnstile } from "../_shared/turnstile.ts";
import { checkRateLimit, rateLimitResponse } from "../_shared/ratelimit.ts";

/** Strip characters that the PostgREST .or()/.ilike() parser treats specially. */
const SAFE_SEARCH_RE = /[^A-Za-z0-9._\-@\s]/g;
function sanitizeSearch(v: unknown, maxLen = 100): string {
  return typeof v === "string" ? v.replace(SAFE_SEARCH_RE, "").slice(0, maxLen) : "";
}

Deno.serve(async (req: Request) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors });
  }

  try {
    const body = await req.json();
    const { password, action, page = 1, per_page = 50, filters, turnstile_token } = body;

    if (!password) {
      return new Response(
        JSON.stringify({ error: "Password required" }),
        { status: 401, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    // Turnstile + IP rate limit defend the password check from brute force.
    const turnstile = await verifyTurnstile(turnstile_token, req);
    if (!turnstile.ok) {
      return new Response(
        JSON.stringify({ error: "Verification failed. Please retry." }),
        { status: 403, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }
    const rl = await checkRateLimit(req, { bucket: "admin-data", max: 20, windowSeconds: 600 });
    if (!rl.ok) return rateLimitResponse(cors, rl.retryAfterSec);

    const supabase = getServiceClient();

    const { data: settings, error: settingsErr } = await supabase
      .from("admin_settings")
      .select("admin_password_hash")
      .eq("id", 1)
      .single();

    if (settingsErr || !settings?.admin_password_hash) {
      return new Response(
        JSON.stringify({ error: "Admin not configured" }),
        { status: 500, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    const ok = await verifyPassword(String(password), settings.admin_password_hash);
    if (!ok) {
      return new Response(
        JSON.stringify({ error: "Invalid password" }),
        { status: 401, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    // Transparent upgrade: if the stored hash is still legacy SHA-256, re-hash
    // with bcrypt now that we've confirmed the plaintext.
    if (!isBcryptHash(settings.admin_password_hash)) {
      try {
        const newHash = await hashPasswordBcrypt(String(password));
        await supabase
          .from("admin_settings")
          .update({ admin_password_hash: newHash })
          .eq("id", 1);
      } catch (e) {
        console.error("bcrypt upgrade failed:", (e as Error).message);
      }
    }

    const safePage = Math.max(1, Math.min(1000, Number(page) || 1));
    const safePerPage = Math.max(1, Math.min(200, Number(per_page) || 50));
    const offset = (safePage - 1) * safePerPage;

    if (action === "leads") {
      let query = supabase
        .from("qualified_leads")
        .select("*", { count: "exact" })
        .order("created_at", { ascending: false })
        .range(offset, offset + safePerPage - 1);

      if (filters?.company_type && typeof filters.company_type === "string") {
        query = query.eq("company_type", filters.company_type.slice(0, 32));
      }
      if (filters?.search) {
        const s = sanitizeSearch(filters.search);
        if (s) {
          // Pass sanitized value into each ilike clause; PostgREST will quote it.
          const pattern = `%${s}%`;
          query = query.or(
            `domain.ilike.${pattern},work_email.ilike.${pattern},company_name.ilike.${pattern}`
          );
        }
      }

      const { data: leads, count, error } = await query;
      if (error) throw error;

      return new Response(
        JSON.stringify({ leads, total: count, page: safePage, per_page: safePerPage }),
        { status: 200, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    if (action === "interactions") {
      let query = supabase
        .from("interaction_logs")
        .select("*", { count: "exact" })
        .order("created_at", { ascending: false })
        .range(offset, offset + safePerPage - 1);

      if (filters?.event_type && typeof filters.event_type === "string") {
        query = query.eq("event_type", filters.event_type.slice(0, 64));
      }
      if (filters?.session_id && typeof filters.session_id === "string") {
        // Session IDs are opaque ASCII tokens; use eq and cap length.
        query = query.eq("session_id", filters.session_id.slice(0, 64));
      }
      if (filters?.source_page) {
        const s = sanitizeSearch(filters.source_page, 200);
        if (s) query = query.ilike("source_page", `%${s}%`);
      }

      const { data: logs, count, error } = await query;
      if (error) throw error;

      return new Response(
        JSON.stringify({ logs, total: count, page: safePage, per_page: safePerPage }),
        { status: 200, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    if (action === "stats") {
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate()).toISOString();
      const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString();

      const [leadsTotal, leadsToday, leadsWeek, interactionsTotal, interactionsToday] =
        await Promise.all([
          supabase.from("qualified_leads").select("*", { count: "exact", head: true }),
          supabase
            .from("qualified_leads")
            .select("*", { count: "exact", head: true })
            .gte("created_at", today),
          supabase
            .from("qualified_leads")
            .select("*", { count: "exact", head: true })
            .gte("created_at", weekAgo),
          supabase.from("interaction_logs").select("*", { count: "exact", head: true }),
          supabase
            .from("interaction_logs")
            .select("*", { count: "exact", head: true })
            .gte("created_at", today),
        ]);

      const { data: topPages } = await supabase
        .from("qualified_leads")
        .select("source_page")
        .order("created_at", { ascending: false })
        .limit(200);

      const pageCounts: Record<string, number> = {};
      (topPages || []).forEach((r: { source_page: string }) => {
        const p = r.source_page || "unknown";
        pageCounts[p] = (pageCounts[p] || 0) + 1;
      });
      const topSourcePages = Object.entries(pageCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([page, count]) => ({ page, count }));

      const { data: typeBreakdown } = await supabase
        .from("qualified_leads")
        .select("company_type");

      const typeCounts: Record<string, number> = {};
      (typeBreakdown || []).forEach((r: { company_type: string }) => {
        typeCounts[r.company_type] = (typeCounts[r.company_type] || 0) + 1;
      });

      return new Response(
        JSON.stringify({
          leads_total: leadsTotal.count || 0,
          leads_today: leadsToday.count || 0,
          leads_week: leadsWeek.count || 0,
          interactions_total: interactionsTotal.count || 0,
          interactions_today: interactionsToday.count || 0,
          top_source_pages: topSourcePages,
          company_types: typeCounts,
        }),
        { status: 200, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ error: "Invalid action. Use: leads, interactions, stats" }),
      { status: 400, headers: { ...cors, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("admin-data error:", (e as Error).message);
    return new Response(
      JSON.stringify({ error: "Server error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } }
    );
  }
});
