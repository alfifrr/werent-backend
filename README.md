# WeRent Backend API

> **Equipment Rental Platform Backend Service**

A modern, secure, and scalable Flask-based backend API for an equipment rental platform. Built with best practices, modular architecture, comprehensive authentication system, and interactive API documentation.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg)](https://flask.palletsprojects.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Authentication-red.svg)](https://jwt.io)
[![Swagger](https://img.shields.io/badge/API-Swagger%20Docs-brightgreen.svg)](http://localhost:5000/docs/)

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

# Run the application
uv run python main.py
```

### Running the Application
```bash
# Development server (preferred)
uv run python main.py

# Alternative method
source .venv/bin/activate
python main.py

# The API will be available at:
# - API: http://localhost:5000
# - Interactive Docs: http://localhost:5000/docs/
# - ReDoc: http://localhost:5000/redoc/
```

## 📋 Features

### ✅ Completed
- **🔐 Complete Authentication System**
  - User registration with comprehensive validation
  - Secure login with JWT tokens (access + refresh)
  - Protected routes and middleware
  - User profile management (GET/PUT)
  - Password hashing with bcrypt
  - Field validation (email, password strength, phone)
  - Error handling with detailed responses

- **📚 Interactive API Documentation**
  - OpenAPI 3.0 specification
  - Swagger UI interface at `/docs/`
  - ReDoc interface at `/redoc/`
  - Comprehensive error response examples
  - Request/response schemas with validation

- **🏗️ Modern Architecture**
  - Application factory pattern
  - Blueprint-based modular routing
  - Pydantic v2 for data validation
  - Standardized API responses
  - Comprehensive input validation
  - Error handling and logging
  - Database migrations with Alembic

- **🗄️ Database Management**
  - SQLAlchemy ORM with enhanced models
  - Database migrations ready
  - User model with proper field structure
  - Active/inactive user states
  - UUID support for users

### 🚧 In Development
- Equipment/Item management system
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
│   │   ├── user.py         # User model with auth methods
│   │   ├── item.py         # Item/Equipment model
│   │   ├── booking.py      # Rental booking model
│   │   └── review.py       # Review and rating model
│   ├── routes/              # Route blueprints
│   │   ├── __init__.py
│   │   ├── main.py         # General routes
│   │   └── auth.py         # Authentication routes
│   ├── schemas/             # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── user_schema.py  # User validation schemas
│   │   └── base_schema.py  # Base validation classes
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   └── user_service.py # User business logic
│   ├── swagger/             # API documentation
│   │   ├── __init__.py
│   │   ├── models.py       # Swagger response models
│   │   └── auth_routes.py  # Auth endpoint documentation
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── validators.py    # Input validation
│       └── responses.py     # API response helpers
├── config/                  # Configuration management
│   ├── __init__.py
│   └── config.py           # Environment configurations
├── docs/                    # Documentation directory
│   ├── dev_notes.md        # Development notes and updates
│   ├── api_documentation.md # Complete API reference
│   ├── project_status.md   # Project status and roadmap
│   └── deployment.md       # Deployment guides
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Test configuration
│   └── test_auth.py        # Authentication tests
├── migrations/              # Database migrations
│   ├── versions/           # Migration files
│   └── env.py             # Migration environment
├── main.py                 # Application entry point
├── pyproject.toml          # Dependencies and project config
└── README.md              # This file
```

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/signup` | User registration | ❌ |
| `POST` | `/api/auth/login` | User authentication | ❌ |
| `GET` | `/api/auth/profile` | Get user profile | ✅ |
| `PUT` | `/api/auth/profile` | Update user profile | ✅ |

### General
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `GET` | `/docs/` | Interactive API documentation (Swagger UI) |
| `GET` | `/redoc/` | Alternative API documentation (ReDoc) |

> **📚 Complete API documentation:** Visit [http://localhost:5000/docs/](http://localhost:5000/docs/) when running the server

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
# Initialize database (automatic on first run)
uv run python main.py

# Run database migrations
uv run flask db upgrade

# Create new migration
uv run flask db migrate -m "Description of changes"
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
DATABASE_URL=sqlite:///werent.db

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

- **[Interactive API Docs](http://localhost:5000/docs/)** - Swagger UI with live testing capability
- **[Alternative API Docs](http://localhost:5000/redoc/)** - ReDoc interface for API reference
- **[docs/api_documentation.md](docs/api_documentation.md)** - Complete API reference with examples
- **[docs/project_status.md](docs/project_status.md)** - Current status, roadmap, and development progress
- **[docs/deployment.md](docs/deployment.md)** - Deployment guides for various platforms
- **[docs/dev_notes.md](docs/dev_notes.md)** - Development notes and recent updates

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

### Phase 2: Equipment Management (Next)
- Equipment catalog with categories
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

> **📋 Detailed roadmap:** See [docs/project_status.md](docs/project_status.md)

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

We welcome contributions! Please see our documentation for guidelines:

- **Development setup:** See [Quick Start](#-quick-start) section above
- **Code style guidelines:** Follow existing patterns and use provided tools
- **Testing requirements:** Add tests for new features
- **Documentation:** Update relevant docs when making changes

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch from `development`
3. Follow code style guidelines (Black formatting)
4. Add tests for new features
5. Update documentation as needed
6. Submit a pull request to `development` branch

### Code Quality Tools
```bash
# Format code
black app/ tests/

# Check style
flake8 app/ tests/

# Run tests with coverage
pytest --cov=app
```

## 📞 Support

- **Interactive Documentation:** [http://localhost:5000/docs/](http://localhost:5000/docs/) (when server is running)
- **API Reference:** Check `docs/api_documentation.md`
- **Development Notes:** See `docs/dev_notes.md` for recent updates
- **Project Status:** Review `docs/project_status.md` for current roadmap

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask framework and ecosystem
- SQLAlchemy for excellent ORM capabilities
- Flask-JWT-Extended for robust JWT implementation
- UV for modern Python package management
- Pydantic for data validation
- OpenAPI/Swagger for API documentation

---

**WeRent Backend API** - Built with ❤️ for the equipment rental community