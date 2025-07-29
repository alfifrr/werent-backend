#!/bin/bash
set -e  # Exit on any error

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

echo "🔄 Syncing dependencies with uv..."
uv sync

echo "🔄 Installing production dependencies..."
uv sync --extra production

echo "🔄 Generating requirements.txt for Render compatibility..."
uv pip freeze > requirements.txt

# Check for new database migrations and run them
echo "🗄️ Checking database migration status..."

# Function to get current migration version from database
get_db_version() {
    uv run python -c "
import sys
import os
import logging

# Suppress Flask app output
logging.getLogger('werkzeug').setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

from flask import Flask
from app import create_app
from app.extensions import db
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext

app = create_app()
with app.app_context():
    try:
        # Get alembic config
        alembic_cfg = Config('migrations/alembic.ini')
        alembic_cfg.set_main_option('script_location', 'migrations')
        
        # Get current revision from database
        from alembic.runtime.migration import MigrationContext
        context = MigrationContext.configure(db.engine.connect())
        current_rev = context.get_current_revision()
        print(current_rev if current_rev else 'None')
    except Exception as e:
        print('None')
        sys.exit(0)
" 2>/dev/null | tail -n 1
}

# Function to get latest migration version from files
get_latest_version() {
    uv run python -c "
from alembic.config import Config
from alembic.script import ScriptDirectory
import sys
import os

try:
    alembic_cfg = Config('migrations/alembic.ini')
    alembic_cfg.set_main_option('script_location', 'migrations')
    script_dir = ScriptDirectory.from_config(alembic_cfg)
    head_rev = script_dir.get_current_head()
    print(head_rev if head_rev else 'None')
except Exception as e:
    print('None')
    sys.exit(0)
" 2>/dev/null | tail -n 1
}

# Get current database version and latest file version
current_db_version=$(get_db_version)
latest_file_version=$(get_latest_version)

echo "� Current database version: $current_db_version"
echo "📍 Latest migration version: $latest_file_version"

# Check if migration is needed
if [ "$current_db_version" != "$latest_file_version" ] || [ "$current_db_version" == "None" ]; then
    echo "🔄 New migration detected! Running database upgrade..."
    echo "   Upgrading from: $current_db_version"
    echo "   Upgrading to:   $latest_file_version"
    
    # Run the migration
    uv run python -m flask db upgrade
    
    # Verify migration success
    new_db_version=$(get_db_version)
    if [ "$new_db_version" == "$latest_file_version" ]; then
        echo "✅ Database migration completed successfully!"
        echo "   Database is now at version: $new_db_version"
    else
        echo "❌ Migration may have failed!"
        echo "   Expected: $latest_file_version"
        echo "   Actual:   $new_db_version"
        exit 1
    fi
else
    echo "✅ Database is already up to date (version: $current_db_version)"
fi

# Run tests to ensure deployment integrity
echo "🧪 Running post-deployment tests..."
export FLASK_ENV=testing
uv run pytest -v -s --cov=. --cov-report term-missing

echo "✅ Build script completed!"