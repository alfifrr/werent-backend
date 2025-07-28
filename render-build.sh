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

echo "✅ Build script completed!"