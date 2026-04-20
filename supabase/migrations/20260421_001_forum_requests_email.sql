-- Add email + ref_code to forum_requests so we can follow up with posters
-- who never join Discord. Email is never sent to Discord; ref_code is a short
-- alphanumeric string shown in the Discord post so admins can correlate a
-- public post back to the private row (and the poster's email).
ALTER TABLE forum_requests ADD COLUMN IF NOT EXISTS email TEXT;
ALTER TABLE forum_requests ADD COLUMN IF NOT EXISTS ref_code TEXT;

CREATE INDEX IF NOT EXISTS idx_forum_requests_ref_code ON forum_requests (ref_code);
CREATE INDEX IF NOT EXISTS idx_forum_requests_email ON forum_requests (email);
