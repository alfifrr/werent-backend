# WeRent Backend API

> **Outfit Rental Platform Backend Service**

A modern, secure, and scalable Flask-based backend API for an outfit rental platform. Built with best practices, modular architecture, and comprehensive authentication system.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg)](https://flask.palletsprojects.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Authentication-red.svg)](https://jwt.io)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- UV package manager
- SQLite (development) / PostgreSQL (production)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd werent-backend

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync

# Initialize database
python main.py
# or
flask init-db
```

### Running the Application
```bash
# Development server
python main.py

# The API will be available at:
# http://localhost:5000
```

## 📋 Features

### ✅ Completed
- **🔐 Complete Authentication System**
  - User registration with validation
  - Secure login with JWT tokens
  - Protected routes and middleware
  - User profile management
  - Password hashing and security

- **🏗️ Modern Architecture**
  - Application factory pattern
  - Blueprint-based modular routing
  - Standardized API responses
  - Comprehensive input validation
  - Error handling and logging

- **🗄️ Database Management**
  - SQLAlchemy ORM with models
  - Database migrations ready
  - Enhanced User model with methods

### 🚧 In Development
- Gear/Equipment management system
- Rental and cart functionality
- Review and rating system
- Admin dashboard
- Payment integration

## 📁 Project Structure

```
werent-backend/
├── app/                      # Main application package
│   ├── __init__.py          # Application factory
│   ├── extensions.py        # Flask extensions
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   └── user.py         # User model
│   ├── routes/              # Route blueprints
│   │   ├── __init__.py
│   │   ├── main.py         # General routes
│   │   └── auth.py         # Authentication routes
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── validators.py    # Input validation
│       └── responses.py     # API response helpers
├── config/                  # Configuration management
│   ├── __init__.py
│   └── config.py           # Environment configurations
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Test configuration
│   └── test_auth.py        # Authentication tests
├── main.py                 # Application entry point
├── pyproject.toml          # Dependencies and project config
├── API_DOCUMENTATION.md    # Complete API documentation
├── PROJECT_STATUS.md       # Project status and roadmap
└── CONTRIBUTING.md         # Development guidelines
```

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/signup` | User registration | ❌ |
| `POST` | `/api/auth/login` | User authentication | ❌ |
| `GET` | `/api/auth/profile` | Get user profile | ✅ |
| `PUT` | `/api/auth/profile` | Update user profile | ✅ |
| `POST` | `/api/auth/logout` | User logout | ✅ |

### General
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `GET` | `/api` | API documentation info |

> **📚 Complete API documentation:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🛠️ Development

### Code Quality Tools
```bash
# Format code
black app/ tests/

# Check style
flake8 app/ tests/

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

### Database Commands
```bash
# Initialize database
flask init-db

# Create admin user
flask create-admin

# Reset database (development)
flask reset-db
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=app --cov-report=html
```

## 🔧 Configuration

### Environment Variables
Copy `.env.template` to `.env` and configure:

```bash
# Flask Configuration
FLASK_SECRET_KEY=your-very-secure-secret-key
FLASK_ENV=development

# JWT Configuration  
JWT_SECRET_KEY=your-jwt-secret-key

# Database Configuration
DATABASE_URL=sqlite:///camrent.db

# Email Configuration (future)
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Configuration Environments
- **Development:** SQLite database, debug mode enabled
- **Testing:** In-memory database, shorter token expiry
- **Production:** PostgreSQL database, enhanced security

## 📖 Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference with examples
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current status, roadmap, and development progress
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines and code standards
- **[GIT_WORKFLOW.md](GIT_WORKFLOW.md)** - Branching strategy and collaboration guidelines

## 🧪 Testing

The project includes comprehensive test coverage with pytest:

- **Unit tests** for models and utilities
- **Integration tests** for API endpoints
- **Authentication flow testing**
- **Input validation testing**
- **Error handling testing**

Example test execution:
```bash
# Run all authentication tests
pytest tests/test_auth.py -v

# Test specific functionality
pytest tests/test_auth.py::TestAuth::test_signup_success
```

## 🚀 Deployment

### Development
- SQLite database
- Flask development server
- Debug mode enabled

### Production (Ready for)
- PostgreSQL database
- Gunicorn WSGI server (included)
- Environment-based configuration
- Docker containerization ready
- SSL/HTTPS configuration

## 🗺️ Roadmap

### Phase 2: Gear Management (Next)
- Gear catalog with categories
- Inventory management
- Search and filtering
- Image upload handling

### Phase 3: Rental System
- Shopping cart functionality
- Checkout and payment processing
- Rental history and management
- Return processing

### Phase 4: Advanced Features
- Review and rating system
- Admin dashboard
- Email notifications
- Advanced reporting

> **📋 Detailed roadmap:** See [PROJECT_STATUS.md](PROJECT_STATUS.md)

## 🌳 Branching Strategy

- `main` – production-ready, protected
- `development` – default active branch for all features
- `feature/<name>` – create branches from `development` for each feature

### Rules:
- Do not push directly to `main`
- All work must be merged into `development` first
- Only the PM may approve and merge changes into `main`

### Workflow:
```bash
# Create feature branch from development
git checkout development
git pull origin development
git checkout -b feature/gear-management

# Work on your feature
git add .
git commit -m "Add gear management endpoints"

# Push feature branch
git push origin feature/gear-management

# Create pull request to development branch
# After review and approval, merge to development
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch
3. Follow code style guidelines
4. Add tests for new features
5. Update documentation
6. Submit a pull request

## 📞 Support

- **Documentation:** Check `API_DOCUMENTATION.md` and `PROJECT_STATUS.md`
- **Code Examples:** See existing implementations in `app/` directory
- **Development Help:** Review `CONTRIBUTING.md`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask framework and ecosystem
- SQLAlchemy for excellent ORM capabilities
- Flask-JWT-Extended for robust JWT implementation
- UV for modern Python package management

---

**CamRent Backend API** - Built with ❤️ for the photography community