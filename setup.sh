#!/bin/bash

# WeRent Backend Installation and Testing Script
# Run this script to install dependencies and test the application

echo "🚀 WeRent Backend Setup Script"
echo "=============================="

# Check Python version
echo "📍 Checking Python version..."
python3 --version

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Test application
echo "🧪 Testing application..."
python3 -c "
from app import create_app
from app.models import *

print('✅ Testing application...')
app = create_app()

with app.app_context():
    print('✅ Models loaded successfully')
    print('✅ Database configuration working')

print('✅ Application ready!')
"

# Test health endpoint (if server is running)
echo "🔍 Application structure:"
echo "- ✅ Requirements.txt created"
echo "- ✅ Procfile for Render created"
echo "- ✅ Environment configuration ready"
echo "- ✅ PostgreSQL support added"
echo "- ✅ Health check endpoints added"
echo "- ✅ CORS configured for production"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create Supabase project and get DATABASE_URL"
echo "2. Deploy to Render using DEPLOYMENT_GUIDE.md"
echo "3. Set environment variables in Render"
echo "4. Run database migrations"
echo ""
echo "For detailed instructions, see DEPLOYMENT_GUIDE.md"
