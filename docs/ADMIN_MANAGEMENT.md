# Admin Management Guide

## Manual Admin Status Changes

Since admin promotion/demotion endpoints have been removed for security reasons, admin status changes are handled via manual database operations.

## Methods for Admin Management

### 1. Using Flask CLI Commands

#### Create New Admin User
```bash
cd /path/to/werent-backend
uv run flask create-admin
```

#### Check Current Admin Status (Python Shell)
```bash
cd /path/to/werent-backend
uv run python -c "
from app import create_app
from app.models.user import User
app = create_app()
with app.app_context():
    admins = User.query.filter_by(is_admin=True).all()
    print('Current Admin Users:')
    for admin in admins:
        print(f'- {admin.email} (ID: {admin.id})')
"
```

### 2. Direct Database Operations

#### Promote User to Admin
```bash
cd /path/to/werent-backend
uv run python -c "
from app import create_app
from app.models.user import User
from app.extensions import db
app = create_app()
with app.app_context():
    user = User.query.filter_by(email='user@example.com').first()
    if user:
        user.is_admin = True
        db.session.commit()
        print(f'User {user.email} promoted to admin')
    else:
        print('User not found')
"
```

#### Demote Admin to Regular User
```bash
cd /path/to/werent-backend
uv run python -c "
from app import create_app
from app.models.user import User
from app.extensions import db
app = create_app()
with app.app_context():
    user = User.query.filter_by(email='admin@example.com').first()
    if user:
        user.is_admin = False
        db.session.commit()
        print(f'User {user.email} demoted from admin')
    else:
        print('User not found')
"
```

### 3. SQL Direct Access (Advanced)

For production environments with direct database access:

#### SQLite (Development)
```sql
-- Promote user to admin
UPDATE users SET is_admin = 1 WHERE email = 'user@example.com';

-- Demote admin to regular user  
UPDATE users SET is_admin = 0 WHERE email = 'admin@example.com';

-- List all admins
SELECT id, email, first_name, last_name, is_admin FROM users WHERE is_admin = 1;
```

#### PostgreSQL (Production)
```sql
-- Promote user to admin
UPDATE users SET is_admin = true WHERE email = 'user@example.com';

-- Demote admin to regular user
UPDATE users SET is_admin = false WHERE email = 'admin@example.com';

-- List all admins
SELECT id, email, first_name, last_name, is_admin FROM users WHERE is_admin = true;
```

## Security Considerations

- **Manual Operations Only**: Admin status changes are intentionally manual to prevent accidental privilege escalation
- **Database Access Required**: These operations require direct database or CLI access, not API access
- **Audit Trail**: Consider logging admin status changes for audit purposes
- **Backup First**: Always backup the database before making admin status changes in production

## Available Admin API Endpoints

The following read-only endpoints are available for admins:

- `GET /api/admin/users` - List all admin users
- `GET /api/admin/users/{id}` - Get specific admin details

These endpoints require admin authentication and are documented in Swagger at `/docs/`.
