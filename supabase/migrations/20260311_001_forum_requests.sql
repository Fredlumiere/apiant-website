-- Forum integration requests from the "Connector Wanted" flow
CREATE TABLE IF NOT EXISTS forum_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  integration_need TEXT NOT NULL,
  source_page TEXT,
  domain TEXT,
  company_type TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_forum_requests_created ON forum_requests (created_at DESC);
