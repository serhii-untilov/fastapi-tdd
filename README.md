# E-commerce API (FastAPI)

This is an e-commerce REST API built with FastAPI, following Test-Driven Development (TDD) practices as part of a Udemy course.

## Project Structure

```
app/
├── database.py          # Database configuration and session management
├── exceptions.py        # Custom exception handlers
├── main.py              # Application entry point and router mounting
├── models/              # SQLAlchemy models (Product, Category, Order, etc.)
├── routers/             # API route definitions
│   ├── products.py      # Product endpoints
│   ├── categories.py    # Category endpoints
│   └── orders.py        # Order endpoints
├── schemas/             # Pydantic models for request/response validation
├── services/            # Business logic layer
├── crud/                # Database operations
└── tests/               # Unit and integration tests

migrations/              # Alembic database migrations
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up database (update `.env` if needed):
   ```bash
   python scripts/init_db.py
   ```

4. Run tests:
   ```bash
   pytest
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `/docs` - Interactive Swagger UI documentation
- `/health` - Health check endpoint
- `/categories/` - Category CRUD operations
- `/products/` - Product management endpoints
- `/orders/` - Order processing endpoints

## Testing Strategy

This project uses pytest with:
- **Unit tests** - Test business logic without database (mocked DB calls)
- **Integration tests** - Use real database to verify full functionality
- **Mocking** - Stub external resources for isolated unit tests

See `tests/` directory for test examples.

## Database

Uses PostgreSQL with SQLAlchemy ORM and Alembic migrations.

## License

MIT