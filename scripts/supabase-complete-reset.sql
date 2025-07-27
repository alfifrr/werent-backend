-- Complete Supabase Database Reset Script
-- Run this in Supabase SQL Editor for thorough cleanup

BEGIN;

-- Drop all tables
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;

-- Drop all ENUM types
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT typname FROM pg_type WHERE typtype = 'e' AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')) LOOP
        EXECUTE 'DROP TYPE IF EXISTS public.' || quote_ident(r.typname) || ' CASCADE';
    END LOOP;
END $$;

-- Drop all sequences
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public') LOOP
        EXECUTE 'DROP SEQUENCE IF EXISTS public.' || quote_ident(r.sequence_name) || ' CASCADE';
    END $$;

-- Drop all views and materialized views
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT table_name FROM information_schema.views WHERE table_schema = 'public') LOOP
        EXECUTE 'DROP VIEW IF EXISTS public.' || quote_ident(r.table_name) || ' CASCADE';
    END LOOP;
END $$;

-- Drop all functions (optional)
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT proname, oidvectortypes(proargtypes) as argtypes FROM pg_proc WHERE pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')) LOOP
        EXECUTE 'DROP FUNCTION IF EXISTS public.' || quote_ident(r.proname) || '(' || r.argtypes || ') CASCADE';
    END LOOP;
END $$;

COMMIT;

-- Verify cleanup
SELECT 'Tables:' as type, count(*) as count FROM pg_tables WHERE schemaname = 'public'
UNION ALL
SELECT 'ENUMs:', count(*) FROM pg_type WHERE typtype = 'e' AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
UNION ALL  
SELECT 'Sequences:', count(*) FROM information_schema.sequences WHERE sequence_schema = 'public'
UNION ALL
SELECT 'Views:', count(*) FROM information_schema.views WHERE table_schema = 'public';
