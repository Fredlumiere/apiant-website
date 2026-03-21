-- Add voice_agent_enabled toggle to admin_settings
-- When false, the "Live Voice Call" (ElevenLabs) option is hidden from leads
ALTER TABLE admin_settings
ADD COLUMN IF NOT EXISTS voice_agent_enabled BOOLEAN DEFAULT true;
