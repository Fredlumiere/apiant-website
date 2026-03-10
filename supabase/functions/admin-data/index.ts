import { getCorsHeaders } from "../_shared/cors.ts";
import { getServiceClient } from "../_shared/supabase.ts";

Deno.serve(async (req: Request) => {
  const cors = getCorsHeaders(req);
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors });
  }

  try {
    const body = await req.json();
    const { password, action, page = 1, per_page = 50, filters } = body;

    if (!password) {
      return new Response(
        JSON.stringify({ error: "Password required" }),
        { status: 401, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    const supabase = getServiceClient();

    // Verify admin password
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

    // Simple password check (bcrypt compare would be ideal, using direct compare for now)
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");

    if (hashHex !== settings.admin_password_hash) {
      return new Response(
        JSON.stringify({ error: "Invalid password" }),
        { status: 401, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    const offset = (page - 1) * per_page;

    if (action === "leads") {
      let query = supabase
        .from("qualified_leads")
        .select("*", { count: "exact" })
        .order("created_at", { ascending: false })
        .range(offset, offset + per_page - 1);

      if (filters?.company_type) {
        query = query.eq("company_type", filters.company_type);
      }
      if (filters?.search) {
        query = query.or(
          `domain.ilike.%${filters.search}%,work_email.ilike.%${filters.search}%,company_name.ilike.%${filters.search}%`
        );
      }

      const { data: leads, count, error } = await query;
      if (error) throw error;

      return new Response(
        JSON.stringify({ leads, total: count, page, per_page }),
        { status: 200, headers: { ...cors, "Content-Type": "application/json" } }
      );
    }

    if (action === "interactions") {
      let query = supabase
        .from("interaction_logs")
        .select("*", { count: "exact" })
        .order("created_at", { ascending: false })
        .range(offset, offset + per_page - 1);

      if (filters?.event_type) {
        query = query.eq("event_type", filters.event_type);
      }
      if (filters?.session_id) {
        query = query.eq("session_id", filters.session_id);
      }
      if (filters?.source_page) {
        query = query.ilike("source_page", `%${filters.source_page}%`);
      }

      const { data: logs, count, error } = await query;
      if (error) throw error;

      return new Response(
        JSON.stringify({ logs, total: count, page, per_page }),
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

      // Top source pages
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

      // Company type breakdown
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
    console.error("Error:", e);
    return new Response(
      JSON.stringify({ error: "Server error" }),
      { status: 500, headers: { ...cors, "Content-Type": "application/json" } }
    );
  }
});
