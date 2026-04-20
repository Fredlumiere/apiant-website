-- Rate-limit tracking table used by edge functions to throttle abusive clients.
-- Each edge-function call that needs throttling inserts one row here. A
-- count-in-window query against (bucket, key) decides whether to allow the
-- request. The table is purged opportunistically on every insert so it
-- doesn't grow unbounded.

create table if not exists rate_limits (
  id bigserial primary key,
  bucket text not null,
  key text not null,
  created_at timestamptz not null default now()
);

create index if not exists rate_limits_lookup_idx
  on rate_limits (bucket, key, created_at desc);

create index if not exists rate_limits_purge_idx
  on rate_limits (created_at);

-- Table is service-role only. Lock out the anon role explicitly.
alter table rate_limits enable row level security;

-- No policies == nothing can read/write except the service role.
