-- Interaction logs: captures every user action in the qualification flow
CREATE TABLE IF NOT EXISTS interaction_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT NOT NULL,               -- unique per popup open
  event_type TEXT NOT NULL,               -- e.g. 'popup_open', 'type_select', 'domain_enter', 'verify_result', etc.
  event_data JSONB DEFAULT '{}',          -- flexible payload for each event type
  source_page TEXT,                       -- which page the event came from
  ip_address TEXT,                        -- visitor IP
  user_agent TEXT,                        -- browser user agent
  referrer TEXT,                          -- HTTP referrer
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_interaction_logs_session ON interaction_logs (session_id);
CREATE INDEX IF NOT EXISTS idx_interaction_logs_created ON interaction_logs (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_interaction_logs_event ON interaction_logs (event_type);
