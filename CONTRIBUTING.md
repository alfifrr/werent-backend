# Contributing to CamRent Backend

Thank you for your interest in contributing to CamRent Backend! This document provides guidelines and instructions for developers working on this project.

## 🏗️ Project Architecture

### Application Structure
```
app/
├── __init__.py           # Application factory
├── extensions.py         # Flask extensions initialization
├── models/              # Database models (SQLAlchemy)
├── routes/              # Route blueprints
├── utils/               # Utility functions and helpers
config/                  # Configuration management
tests/                   # Test suites
```

### Key Principles
- **Blueprint-based routing** for modular organization
- **Application factory pattern** for flexible app creation
- **Standardized API responses** using utility functions
- **Comprehensive input validation** for security
- **Type hints** for better code documentation
- **Docstrings** for all public functions and classes

## 🚀 Getting Started

### 1. Environment Setup
```bash
# Clone and navigate to project
cd /home/alfi/Projects/werent-backend

# Activate virtual environment
source .venv/bin/activate

# Install dependencies including dev tools
uv sync
```

### 2. Development Tools
```bash
# Format code
black app/ tests/

# Check code style
flake8 app/ tests/

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

### 3. Database Management
```bash
# Initialize database
flask init-db

# Create admin user
flask create-admin

# Reset database (development only)
flask reset-db
```

## 📝 Development Guidelines

### Code Style
- Follow **PEP 8** style guidelines
- Use **meaningful variable and function names**
- Maximum line length: 88 characters (Black default)
- Use **type hints** where appropriate
- Add **docstrings** for all public functions

### Example Function Format
```python
def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None
```

### API Response Standards
Always use the standardized response utilities:

```python
from app.utils import success_response, error_response, validation_error_response

# Success response
return success_response(
    message="Operation successful",
    data={"user": user.to_dict()},
    status_code=200
)

# Error response
return error_response(
    message="Invalid input",
    status_code=400,
    error_code="VALIDATION_ERROR"
)

# Validation error with field details
return validation_error_response(
    field_errors={"email": "Invalid format"},
    message="Validation failed"
)
```

### Database Models
- Use descriptive table names
- Include `created_at` and `updated_at` timestamps
- Add proper indexes for frequently queried fields
- Implement useful methods (`to_dict()`, `find_by_*()`, etc.)

```python
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email address."""
        return cls.query.filter_by(email=email.lower().strip()).first()
```

## 🧪 Testing Guidelines

### Test Structure
- Tests should be in the `tests/` directory
- Use descriptive test names: `test_signup_success`, `test_login_invalid_credentials`
- Group related tests in classes
- Use fixtures for common setup

### Example Test
```python
class TestAuth:
    def test_signup_success(self, client):
        """Test successful user registration."""
        data = {
            'email': 'test@camrent.com',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        response = client.post('/api/auth/signup', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['success'] is True
        assert 'access_token' in json_data['data']
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_auth.py::TestAuth::test_signup_success
```

## 🔄 Adding New Features

### 1. Creating New Models
1. Add model file to `app/models/`
2. Import in `app/models/__init__.py`
3. Create database migration (future: use Flask-Migrate)

### 2. Creating New Routes
1. Create blueprint file in `app/routes/`
2. Register blueprint in `app/routes/__init__.py`
3. Use standardized response utilities
4. Add proper error handling
5. Validate all inputs

### 3. Example New Route Blueprint
```python
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import success_response, error_response
from app.models import User

# Create blueprint
gear_bp = Blueprint('gear', __name__, url_prefix='/api/gear')

@gear_bp.route('/', methods=['GET'])
def list_gear():
    """List all available gear."""
    try:
        # Implementation here
        return success_response(
            message="Gear list retrieved successfully",
            data={"gear": []}
        )
    except Exception as e:
        return error_response("Internal server error", 500)
```

### 4. Adding Input Validation
```python
from app.utils import validate_email, validate_name, sanitize_string

# Validate and sanitize inputs
email = sanitize_string(data.get('email', ''))
if not validate_email(email):
    field_errors['email'] = 'Invalid email format'

first_name = sanitize_string(data.get('first_name', ''))
is_valid, error_msg = validate_name(first_name, "First name")
if not is_valid:
    field_errors['first_name'] = error_msg
```

## 📋 Checklist for New Features

### Before Implementation
- [ ] Feature is documented in PROJECT_STATUS.md roadmap
- [ ] Database schema changes are planned
- [ ] API endpoints are designed
- [ ] Input validation requirements identified

### During Implementation
- [ ] Follow existing code patterns
- [ ] Use standardized response utilities
- [ ] Implement proper error handling
- [ ] Add input validation and sanitization
- [ ] Write comprehensive tests
- [ ] Add type hints and docstrings

### After Implementation
- [ ] All tests pass
- [ ] Code passes linting (flake8)
- [ ] Code is formatted (black)
- [ ] Update PROJECT_STATUS.md
- [ ] Update API_DOCUMENTATION.md
- [ ] Manual testing completed

## 🌳 Git Workflow & Branching Strategy

### Branch Structure
- **`main`** – Production-ready code, protected branch
- **`development`** – Default active branch for all features and integration
- **`feature/<name>`** – Feature branches created from `development`

### Branching Rules
- ❌ **Do not push directly to `main`**
- ✅ All work must be merged into `development` first
- ✅ Only the Project Manager (PM) may approve and merge changes into `main`
- ✅ Create feature branches from `development`
- ✅ Use descriptive feature branch names (e.g., `feature/gear-management`, `feature/user-authentication`)

### Development Workflow
```bash
# 1. Start new feature
git checkout development
git pull origin development
git checkout -b feature/your-feature-name

# 2. Work on your feature
# Make changes, add tests, update documentation

# 3. Commit your changes
git add .
git commit -m "feat: add gear management endpoints"

# 4. Push feature branch
git push origin feature/your-feature-name

# 5. Create Pull Request
# - Target: development branch
# - Include description of changes
# - Link to related issues
# - Request code review

# 6. After approval and merge to development
git checkout development
git pull origin development
git branch -d feature/your-feature-name
```

### Commit Message Convention
Use conventional commits for clear history:
```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code refactoring
test: adding tests
chore: maintenance tasks
```

### Pull Request Guidelines
- **Target Branch:** Always target `development` for feature PRs
- **Title:** Use clear, descriptive titles
- **Description:** Explain what changes were made and why
- **Testing:** Ensure all tests pass
- **Documentation:** Update relevant documentation
- **Review:** Request review from team members

### Code Review Process
1. **Developer** creates PR to `development`
2. **Team members** review code
3. **Tests** must pass
4. **Documentation** must be updated
5. **Approval** required before merge
6. **PM approval** required for `development` → `main` merges

## 🐛 Bug Reports and Issues

### Reporting Bugs
1. Check if the issue already exists
2. Provide clear reproduction steps
3. Include error messages and logs
4. Specify environment details

### Bug Fix Process
1. Write a test that reproduces the bug
2. Fix the issue
3. Ensure the test passes
4. Verify no regressions occurred

## 🔒 Security Guidelines

### Input Validation
- **Always validate** user inputs
- **Sanitize** string inputs
- **Use parameterized queries** (SQLAlchemy handles this)
- **Validate file uploads** (when implemented)

### Authentication
- **Never store plain text passwords**
- **Use secure JWT tokens**
- **Implement proper session management**
- **Validate tokens on protected routes**

### Error Handling
- **Don't expose sensitive information** in error messages
- **Log errors** appropriately
- **Use standardized error responses**

## 📚 Resources

### Documentation
- `API_DOCUMENTATION.md` - Complete API reference
- `PROJECT_STATUS.md` - Project status and roadmap
- Flask documentation: https://flask.palletsprojects.com/
- SQLAlchemy documentation: https://docs.sqlalchemy.org/

### Tools
- **Black**: Code formatter
- **Flake8**: Style checker
- **Pytest**: Testing framework
- **UV**: Package manager

## 🤝 Code Review Process

### For Pull Requests
1. Ensure all tests pass
2. Code follows style guidelines
3. Documentation is updated
4. Changes are covered by tests
5. Security implications considered

### Review Checklist
- [ ] Code follows project patterns
- [ ] Proper error handling implemented
- [ ] Input validation added
- [ ] Tests cover new functionality
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced

---

## 🆘 Getting Help

If you need help or have questions:

1. Check existing documentation
2. Review similar implementations in the codebase
3. Check the project structure for patterns
4. Refer to Flask and SQLAlchemy documentation

Remember: This project uses a modular architecture with standardized patterns. When in doubt, follow existing patterns in the codebase!

---

*Happy coding! 🚀*
