#!/bin/bash
# Migration Management Script for WeRent Backend
# This script helps manage database migrations for local development and deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}📍${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Function to check if virtual environment is activated
check_env() {
    if command -v uv &> /dev/null; then
        print_status "Using uv for package management"
        python_cmd="uv run python"
        flask_cmd="uv run python -m flask"
    elif [[ "$VIRTUAL_ENV" != "" ]]; then
        print_status "Virtual environment detected: $VIRTUAL_ENV"
        python_cmd="python"
        flask_cmd="flask"
    else
        print_error "No virtual environment detected and uv not available!"
        print_error "Please activate your virtual environment or install uv"
        exit 1
    fi
}

# Function to get current migration version from database
get_db_version() {
    $python_cmd -c "
import sys
import os
import logging

# Suppress Flask app output
logging.getLogger('werkzeug').setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

from flask import Flask
from app import create_app
from app.extensions import db
from alembic.runtime.migration import MigrationContext

app = create_app()
with app.app_context():
    try:
        context = MigrationContext.configure(db.engine.connect())
        current_rev = context.get_current_revision()
        print(current_rev if current_rev else 'None')
    except Exception as e:
        print('None')
" 2>/dev/null | tail -n 1
}

# Function to get latest migration version from files
get_latest_version() {
    $python_cmd -c "
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
" 2>/dev/null | tail -n 1
}

# Function to show migration status
show_status() {
    print_status "Migration Status Check"
    echo "========================"
    
    current_db=$(get_db_version)
    latest_file=$(get_latest_version)
    
    echo "Current database version: $current_db"
    echo "Latest migration version: $latest_file"
    echo ""
    
    if [ "$current_db" == "$latest_file" ] && [ "$current_db" != "None" ]; then
        print_success "Database is up to date!"
    elif [ "$current_db" == "None" ]; then
        print_warning "Database not initialized. Run 'upgrade' to apply migrations."
    else
        print_warning "Database needs migration from $current_db to $latest_file"
        echo "Run 'upgrade' to apply pending migrations."
    fi
}

# Function to create new migration
create_migration() {
    local message="$1"
    if [ -z "$message" ]; then
        print_error "Migration message is required!"
        echo "Usage: $0 migrate \"your migration message\""
        exit 1
    fi
    
    print_status "Creating new migration: $message"
    $flask_cmd db migrate -m "$message"
    
    # Show what was created
    latest=$(get_latest_version)
    if [ "$latest" != "None" ]; then
        print_success "Created migration: $latest"
        print_warning "Don't forget to review the generated migration file!"
        echo "Location: migrations/versions/${latest}_*.py"
    fi
}

# Function to upgrade database
upgrade_db() {
    print_status "Upgrading database to latest migration..."
    $flask_cmd db upgrade
    
    # Verify upgrade
    current_db=$(get_db_version)
    latest_file=$(get_latest_version)
    
    if [ "$current_db" == "$latest_file" ]; then
        print_success "Database upgraded successfully to version: $current_db"
    else
        print_error "Migration may have failed!"
        echo "Expected: $latest_file"
        echo "Actual: $current_db"
        exit 1
    fi
}

# Function to stamp database with current migration version
stamp_db() {
    local version="$1"
    if [ -z "$version" ]; then
        # Get the latest version if none specified
        version=$(get_latest_version)
        if [ "$version" == "None" ]; then
            print_error "No migration version found to stamp with!"
            exit 1
        fi
    fi
    
    print_status "Stamping database with version: $version"
    $flask_cmd db stamp "$version"
    
    # Verify stamp
    current_db=$(get_db_version)
    if [ "$current_db" == "$version" ]; then
        print_success "Database stamped successfully with version: $current_db"
    else
        print_error "Stamp may have failed!"
        echo "Expected: $version"
        echo "Actual: $current_db"
        exit 1
    fi
}

# Function to fix database that has tables but no alembic tracking
fix_db() {
    print_status "Checking if database needs to be fixed..."
    
    current_db=$(get_db_version)
    latest_file=$(get_latest_version)
    
    if [ "$current_db" == "None" ] && [ "$latest_file" != "None" ]; then
        print_warning "Database has no alembic tracking but migration files exist"
        print_status "This usually means database was created without migrations"
        
        # Check if tables exist
        has_tables=$($python_cmd -c "
import sys
import os
import logging

# Suppress Flask app output
logging.getLogger('werkzeug').setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        try:
            result = conn.execute(text('SELECT name FROM sqlite_master WHERE type=\'table\' AND name != \'alembic_version\';'))
            tables = [row[0] for row in result.fetchall()]
            print('yes' if len(tables) > 0 else 'no')
        except Exception:
            print('no')
" 2>/dev/null | tail -n 1)
        
        if [ "$has_tables" == "yes" ]; then
            print_warning "Tables exist but no alembic tracking found"
            print_status "Stamping database with current migration version: $latest_file"
            stamp_db "$latest_file"
        else
            print_status "No tables found - running normal upgrade"
            upgrade_db
        fi
    else
        print_success "Database tracking is consistent - no fix needed"
    fi
}

# Function to simulate deployment migration check
simulate_deployment() {
    print_status "Simulating Render deployment migration check..."
    echo "=================================================="
    
    current_db=$(get_db_version)
    latest_file=$(get_latest_version)
    
    echo "📍 Current database version: $current_db"
    echo "📍 Latest migration version: $latest_file"
    
    if [ "$current_db" != "$latest_file" ] || [ "$current_db" == "None" ]; then
        print_warning "Migration would be triggered on deployment!"
        echo "   Upgrading from: $current_db"
        echo "   Upgrading to:   $latest_file"
        echo ""
        echo "This is what would happen on Render:"
        echo "1. render-build.sh would detect version mismatch"
        echo "2. flask db upgrade would be executed"
        echo "3. Supabase database would be updated"
        echo ""
        print_warning "Make sure to test this migration locally first!"
    else
        print_success "No migration needed - database is up to date"
        echo "Deployment would skip migration step."
    fi
}

# Function to show help
show_help() {
    echo "WeRent Backend Migration Management"
    echo "=================================="
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  status                    Show current migration status"
    echo "  migrate \"message\"         Create new migration with message"
    echo "  upgrade                   Apply pending migrations to database"
    echo "  stamp [version]           Mark database as having specific migration version"
    echo "  fix                       Fix database that has tables but no alembic tracking"
    echo "  simulate                  Simulate what would happen on deployment"
    echo "  help                      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 status"
    echo "  $0 migrate \"Add user profile fields\""
    echo "  $0 upgrade"
    echo "  $0 stamp 04f23c4db7a1"
    echo "  $0 fix"
    echo "  $0 simulate"
}

# Main script logic
check_env

case "${1:-help}" in
    "status")
        show_status
        ;;
    "migrate")
        create_migration "$2"
        ;;
    "upgrade")
        upgrade_db
        ;;
    "stamp")
        stamp_db "$2"
        ;;
    "fix")
        fix_db
        ;;
    "simulate")
        simulate_deployment
        ;;
    "help"|*)
        show_help
        ;;
esac
