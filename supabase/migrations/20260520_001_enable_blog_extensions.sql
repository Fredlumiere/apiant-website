-- Enable extensions required by the blog publish trigger
-- pg_net: HTTP requests from triggers (used to POST repository_dispatch)
-- vault:  encrypted secret storage (used to hold github_dispatch_pat)
CREATE EXTENSION IF NOT EXISTS pg_net WITH SCHEMA extensions;
CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA vault;
