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

# Run database migrations (if needed)
echo "🔄 Running database migrations..."
uv run python -m flask db upgrade

# Run tests to ensure deployment integrity
echo "🧪 Running post-deployment tests..."
export FLASK_ENV=testing
uv run pytest -v -s --cov=. --cov-report term-missing

echo "✅ Build script completed!"