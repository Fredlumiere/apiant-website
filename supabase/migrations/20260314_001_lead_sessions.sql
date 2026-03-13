-- Lead sessions for WhatsApp handoff flow
-- Stores qualified lead context for ElevenLabs AI agent retrieval

CREATE TABLE IF NOT EXISTS lead_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT UNIQUE NOT NULL,            -- short token: apt_XXXXXXXX
  company_type TEXT NOT NULL,                 -- saas, si, enterprise
  domain TEXT,
  company_description TEXT,                   -- from Firecrawl/Haiku verification
  detected_type TEXT,                         -- from verify-company-type
  contact_email TEXT NOT NULL,
  contact_name TEXT,                          -- first + last from form
  company_name TEXT,
  integration_needs TEXT,                     -- free-text from form
  source_page TEXT,                           -- which page they came from
  whatsapp_opened BOOLEAN DEFAULT false,      -- set true when agent receives message
  agent_conversation_status TEXT DEFAULT 'pending'
    CHECK (agent_conversation_status IN ('pending', 'active', 'completed', 'handed_off')),
  handed_off_to TEXT,                         -- 'founder_call', 'calendly', null
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_lead_sessions_session_id ON lead_sessions (session_id);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_created_at ON lead_sessions (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_status ON lead_sessions (agent_conversation_status);
