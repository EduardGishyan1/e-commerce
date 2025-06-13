# E-Commerce Backend System

## Project Overview

This repository contains the backend implementation for an e-commerce platform using **FastAPI**, **Pydantic**, and **SQLAlchemy**. The project is designed to demonstrate industry-level practices, focusing on modularity, scalability, and security.

## Features

- **Authentication and Authorization**
  - JWT-based authentication and role-based access control (Admin, Vendor, Customer).
- **Product Management**
  - CRUD operations for products, with support for filtering and pagination.
- **Cart and Order Processing**
  - Shopping cart functionality and secure order management.
- **Admin Panel**
  - Analytics and reporting capabilities for administrators.
- **Database Management**
  - PostgreSQL integration with SQLAlchemy ORM and Alembic migrations.

---

## Folder Structure

### Root-Level Files:
- **`.env`**: Stores environment variables (e.g., secrets, database URL). Keep this out of version control.
- **`README.md`**: Comprehensive guide to the project.
- **`requirements.txt`**: Contains all dependencies for the project.
- **`alembic/`**: Database migrations directory.

### Application Directory (`app/`):
- **`main.py`**: Entry point of the FastAPI application.
- **`config/`**: Contains configuration files.
  - **`settings.py`**: Centralized configuration, like database connection URL or JWT secret.
- **`routers/`**: Contains API endpoint routers organized by features.
  - Examples: `auth.py`, `users.py`, `products.py`, `orders.py`, `admin.py`.
- **`models/`**: SQLAlchemy models defining database tables.
  - Examples: `user.py`, `product.py`, `order.py`.
- **`schemas/`**: Pydantic schemas for request/response validation and serialization.
  - Examples: `user.py`, `product.py`, `order.py`.
- **`services/`**: Business logic functions separated from routers for reusability and clarity.
  - Examples: `auth_service.py`, `user_service.py`, `order_service.py`.
- **`utils/`**: Utility functions like hashing, token generation, and pagination.
  - Examples: `hashing.py`, `token.py`, `pagination.py`.
- **`database/`**: Manages database session and connection.
  - **`session.py`**: SQLAlchemy session setup.
- **`middlewares/`**: Custom middleware like rate limiting.
  - Example: `rate_limiter.py`.

### Other Directories:

- **`logs/`**: Centralized logging for easier debugging.
  - Example: `app.log`.

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Code-Republic-Community/e-commerce
   cd ecommerce-backend
   ```
2. Create and configure the `.env` file with necessary environment variables:
   ```
   DATABASE_URL=<your-database-url>
   JWT_SECRET_KEY=<your-secret-key>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Access the API documentation:
   - Swagger UI: `https://e-commerce-api.coderepublic.am/docs`
   - ReDoc: `https://e-commerce-api.coderepublic.am/redoc`

---

## Contribution Guidelines

- Follow PEP 8 guidelines for code style.
- Submit pull requests with detailed descriptions for changes.
- Write tests for new functionality and ensure all tests pass before merging.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.

