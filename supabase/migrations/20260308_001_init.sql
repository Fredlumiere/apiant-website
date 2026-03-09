-- APIANT Website Backend: Initial schema
-- Tables for lead qualification flow, OTP verification, and admin settings

-- Admin settings (availability toggle, business hours)
CREATE TABLE IF NOT EXISTS admin_settings (
  id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),  -- singleton row
  available BOOLEAN NOT NULL DEFAULT false,
  timezone TEXT NOT NULL DEFAULT 'America/New_York',
  business_hours_start TIME NOT NULL DEFAULT '09:00',
  business_hours_end TIME NOT NULL DEFAULT '17:00',
  business_days INTEGER[] NOT NULL DEFAULT ARRAY[1,2,3,4,5],  -- 0=Sun, 1=Mon ... 6=Sat
  calendly_url TEXT DEFAULT '',
  admin_password_hash TEXT NOT NULL,  -- bcrypt hash for admin auth
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Insert default row
INSERT INTO admin_settings (id, admin_password_hash)
VALUES (1, '')  -- Password must be set during setup
ON CONFLICT (id) DO NOTHING;

-- OTP codes for phone/email verification
CREATE TABLE IF NOT EXISTS otp_codes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact TEXT NOT NULL,              -- email or phone number
  contact_type TEXT NOT NULL CHECK (contact_type IN ('email', 'sms', 'whatsapp')),
  code TEXT NOT NULL,                 -- 6-digit code
  session_id TEXT NOT NULL,           -- ties OTP to a specific form session
  verified BOOLEAN NOT NULL DEFAULT false,
  attempts INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at TIMESTAMPTZ NOT NULL DEFAULT (now() + INTERVAL '10 minutes')
);

-- Auto-cleanup expired OTPs
CREATE INDEX IF NOT EXISTS idx_otp_codes_expires ON otp_codes (expires_at);
CREATE INDEX IF NOT EXISTS idx_otp_codes_session ON otp_codes (session_id);

-- Qualified leads
CREATE TABLE IF NOT EXISTS qualified_leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_type TEXT NOT NULL CHECK (company_type IN ('saas', 'si', 'enterprise')),
  domain TEXT NOT NULL,
  domain_verified BOOLEAN NOT NULL DEFAULT false,
  verification_result JSONB,          -- AI analysis result
  work_email TEXT,
  company_name TEXT,
  integration_needs TEXT,
  phone TEXT,
  phone_type TEXT CHECK (phone_type IN ('email', 'sms', 'whatsapp')),
  phone_verified BOOLEAN NOT NULL DEFAULT false,
  wants_call_now BOOLEAN DEFAULT false,
  source_page TEXT,                   -- which page they came from
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_qualified_leads_created ON qualified_leads (created_at DESC);

-- Cleanup function: delete expired OTPs older than 1 hour
CREATE OR REPLACE FUNCTION cleanup_expired_otps()
RETURNS void AS $$
BEGIN
  DELETE FROM otp_codes WHERE expires_at < now() - INTERVAL '1 hour';
END;
$$ LANGUAGE plpgsql;
