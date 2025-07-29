# Database Migration Workflow for WeRent Backend

## 🎯 Overview

This document explains how the enhanced database migration system works for the WeRent backend, especially for deployments from Render to Supabase.

## 🔄 How It Works

### Current State
- **Local database**: Alembic version `04f23c4db7a1`
- **Supabase database**: Alembic version `04f23c4db7a1` 
- **Status**: ✅ Both databases are synchronized

### Automatic Migration Trigger

The enhanced `render-build.sh` script now automatically detects when migrations are needed:

1. **Version Check**: Compares database version vs. latest migration file
2. **Smart Migration**: Only runs `flask db upgrade` when versions don't match
3. **Verification**: Confirms migration success before proceeding
4. **Logging**: Provides detailed migration status during deployment

## 🛠️ Development Workflow

### 1. Creating New Migrations (Local)

When you modify models locally:

```bash
# Option 1: Use the migration manager script
./scripts/migration-manager.sh migrate "Add new user fields"

# Option 2: Use Flask-Migrate directly
uv run python -m flask db migrate -m "Add new user fields"
```

### 2. Testing Migrations Locally

```bash
# Check current status
./scripts/migration-manager.sh status

# Apply migrations locally
./scripts/migration-manager.sh upgrade

# Or use Flask directly
uv run python -m flask db upgrade
```

### 3. Simulating Deployment

Before pushing to Git, simulate what will happen on Render:

```bash
# This shows what the deployment would do
./scripts/migration-manager.sh simulate
```

### 4. Deploying to Production

When you push to your deployment branch:

1. **Render Build Phase**: `render-build.sh` runs automatically
2. **Migration Detection**: Script compares versions
3. **Automatic Migration**: If new version found, runs `flask db upgrade`
4. **Supabase Update**: Your Supabase database gets updated
5. **Verification**: Confirms migration success

## 📋 Example Scenarios

### Scenario 1: No Changes Needed
```bash
# Current state
Database version: 04f23c4db7a1
Latest file version: 04f23c4db7a1

# Deployment output
✅ Database is already up to date (version: 04f23c4db7a1)
```

### Scenario 2: New Migration Available
```bash
# After creating new migration locally
Database version: 04f23c4db7a1
Latest file version: 1a2b3c4d5e6f

# Deployment output
🔄 New migration detected! Running database upgrade...
   Upgrading from: 04f23c4db7a1
   Upgrading to:   1a2b3c4d5e6f
✅ Database migration completed successfully!
```

### Scenario 3: Fresh Database
```bash
# If Supabase database is empty
Database version: None
Latest file version: 04f23c4db7a1

# Deployment output
🔄 New migration detected! Running database upgrade...
   Upgrading from: None
   Upgrading to:   04f23c4db7a1
✅ Database migration completed successfully!
```

## 🔧 Migration Manager Script Usage

The `scripts/migration-manager.sh` script provides easy migration management:

```bash
# Check migration status
./scripts/migration-manager.sh status

# Create new migration
./scripts/migration-manager.sh migrate "Your migration message"

# Apply pending migrations
./scripts/migration-manager.sh upgrade

# Simulate deployment behavior
./scripts/migration-manager.sh simulate

# Show help
./scripts/migration-manager.sh help
```

## ⚠️ Important Notes

### Before Creating Migrations:
1. **Test Model Changes**: Ensure your model changes work locally
2. **Review Generated Migration**: Always check the auto-generated migration file
3. **Test Migration**: Run the migration locally before deploying

### Before Deployment:
1. **Simulate First**: Use `./scripts/migration-manager.sh simulate`
2. **Check Status**: Ensure local and production are properly versioned
3. **Backup Database**: Consider backing up Supabase data for critical migrations

### During Deployment:
- Monitor Render build logs for migration status
- Check for any migration errors in the deployment logs
- Verify database schema in Supabase dashboard after deployment

## 🚨 Troubleshooting

### Migration Fails During Deployment
```bash
# Check logs in Render dashboard
# Look for migration errors
# Verify DATABASE_URL is correct
```

### Version Mismatch Issues
```bash
# Reset local database to match production (if needed)
./scripts/migration-manager.sh status

# Or manually check versions
uv run python -m flask db current
```

### Manual Migration in Production
If you need to run migrations manually on Render:

1. Go to Render Dashboard → Your Service → Shell
2. Run: `flask db upgrade`
3. Verify: `flask db current`

## 🎯 Benefits of This System

✅ **Automatic**: No manual migration steps needed during deployment  
✅ **Safe**: Only runs migrations when actually needed  
✅ **Logged**: Clear migration status in deployment logs  
✅ **Verified**: Confirms migration success before continuing  
✅ **Flexible**: Works with any Alembic version changes  

## 📝 Files Modified

- **`render-build.sh`**: Enhanced with automatic migration detection
- **`scripts/migration-manager.sh`**: New script for local migration management
- **`docs/MIGRATION_WORKFLOW.md`**: This documentation file

---

**🎯 Ready to automatically handle database migrations from Render to Supabase!**
