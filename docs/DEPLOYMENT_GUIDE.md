# WeRent Backend Deployment Guide

This guide will help you deploy the WeRent Backend API to Render with Supabase PostgreSQL database.

## Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Supabase Account** - Sign up at [supabase.com](https://supabase.com)

## Step 1: Set up Supabase Database

1. **Create a new Supabase project:**
   - Go to [supabase.com](https://supabase.com)
   - Click "New Project"
   - Choose your organization
   - Enter project name: `werent-database`
   - Enter database password (save this!)
   - Select region closest to your users

2. **Get your database connection string:**
   - Go to Project Settings → Database
   - Copy the "Connection string" under "Connection pooling"
   - It should look like: `postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres`

3. **Configure database (optional):**
   - You can use the SQL Editor in Supabase to run custom queries
   - The Flask migrations will handle table creation

## Step 2: Deploy to Render

1. **Connect your GitHub repository:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your `werent-backend` repository

2. **Configure the deployment:**
   ```
   Name: werent-backend-api
   Environment: Python 3
   Branch: main (or your preferred branch)
   Root Directory: (leave blank if backend is in root)
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn main:app --bind 0.0.0.0:$PORT --workers 4
   ```

3. **Set environment variables in Render:**
   Go to Environment section and add these variables:
   
   ```bash
   FLASK_ENV=production
   FLASK_SECRET_KEY=your-super-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres
   FRONTEND_URL=https://your-frontend-domain.com
   ```

   **Important Notes:**
   - Generate strong random keys for `FLASK_SECRET_KEY` and `JWT_SECRET_KEY`
   - Use the connection string from Supabase for `DATABASE_URL`
   - Update `FRONTEND_URL` with your actual frontend domain

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

## Step 3: Run Database Migrations

After deployment, you need to initialize your database:

1. **Access Render Shell:**
   - Go to your service dashboard in Render
   - Click "Shell" tab
   - Run the following commands:

   ```bash
   # Initialize migrations (if not already done)
   flask db init
   
   # Create migration for current models
   flask db migrate -m "Initial migration"
   
   # Apply migrations to database
   flask db upgrade
   
   # Create an admin user (optional)
   flask create-admin
   ```

## Step 4: Test Your Deployment

1. **Check service status:**
   - Your API should be accessible at: `https://your-service-name.onrender.com`
   - Test the health endpoint: `https://your-service-name.onrender.com/api/health`

2. **Test API endpoints:**
   ```bash
   # Test registration
   curl -X POST https://your-service-name.onrender.com/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"testpass123","first_name":"Test","last_name":"User"}'
   
   # Test login
   curl -X POST https://your-service-name.onrender.com/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"testpass123"}'
   ```

## Step 5: Update Frontend Configuration

Update your frontend application to use the new backend URL:

```javascript
// In your frontend environment configuration
const API_BASE_URL = 'https://your-service-name.onrender.com/api';
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_SECRET_KEY` | Flask secret key | `your-secret-key` |
| `JWT_SECRET_KEY` | JWT secret key | `your-jwt-secret` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `FRONTEND_URL` | Frontend application URL | `https://example.com` |

## Troubleshooting

### Common Issues:

1. **Database Connection Error:**
   - Verify your `DATABASE_URL` is correct
   - Check that Supabase project is active
   - Ensure connection string includes the correct password

2. **Build Failures:**
   - Check that `requirements.txt` is present and complete
   - Verify Python version compatibility
   - Look at build logs in Render dashboard

3. **Migration Errors:**
   - Run `flask db upgrade` in Render shell
   - Check database permissions in Supabase
   - Verify migration files exist

4. **CORS Errors:**
   - Update `FRONTEND_URL` environment variable
   - Check CORS configuration in `app/utils/cors.py`

### Monitoring:

- **Render Dashboard:** Monitor service health, logs, and metrics
- **Supabase Dashboard:** Monitor database performance and usage
- **Logs:** Check application logs in Render for errors

## Security Considerations

1. **Secrets Management:**
   - Never commit secrets to Git
   - Use strong, randomly generated keys
   - Rotate secrets regularly

2. **Database Security:**
   - Use Supabase's built-in security features
   - Enable Row Level Security (RLS) if needed
   - Monitor database access logs

3. **API Security:**
   - HTTPS is enforced by Render
   - JWT tokens have expiration times
   - Implement rate limiting if needed

## Scaling

- **Render:** Upgrade to higher plans for more resources
- **Supabase:** Monitor database usage and upgrade as needed
- **CDN:** Consider adding a CDN for static assets

## Backup Strategy

- **Database:** Supabase provides automatic backups
- **Code:** Ensure code is backed up in Git
- **Environment Variables:** Document all variables securely
