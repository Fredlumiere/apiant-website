-- Add admin_email column and set initial credentials
ALTER TABLE admin_settings ADD COLUMN IF NOT EXISTS admin_email TEXT;

UPDATE admin_settings
SET admin_email = 'fred@apiant.com',
    admin_password_hash = '7486e9e174c8a07c031abf4d0d4799b2aec2eee20a2a55991f85935ebfa7ee13'
WHERE id = 1;
