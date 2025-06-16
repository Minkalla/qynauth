# Minkalla QynAuth

Quantum-Resistant Authentication Microservice (Python FastAPI / Rust)

## Project Status

[![Under Active Development](https://img.shields.io/badge/status-under%20active%20development-orange)](https://github.com/minkalla/qynauth)

This project is currently under active development as part of the Minkalla MVP.

## Overview

QynAuth is a foundational component of the Minkalla ecosystem, focused on providing future-proof authentication and identity management. This MVP version implements secure classical authentication methods and includes a placeholder for advanced quantum-resistant cryptography, demonstrating readiness for post-quantum security challenges.

## Features (MVP)

* **User Registration:** `POST /auth/register` to securely register new user accounts (in-memory storage for MVP).
* **User Login & JWT Generation:** `POST /auth/login` to authenticate users and issue JSON Web Tokens (JWT) for API access.
* **Health Check:** `GET /health` to verify service operational status.
* **Quantum-Safe Placeholder:** Integration with a Rust library for future quantum-resistant cryptographic operations, showing the modular architecture.
* **API Documentation:** Built-in Swagger UI for easy API exploration.
* **Unit Tested:** Core API endpoints are covered by comprehensive unit tests.

## Getting Started

### Prerequisites

* Python 3.10+ and Poetry installed.
* Rust toolchain (rustup, cargo) installed.
* (Optional but Recommended for Development): GitHub Codespaces for a pre-configured cloud development environment. A `.devcontainer` configuration is included for easy setup.

### Local Development Setup (Using Codespaces)

If you are using GitHub Codespaces, the environment (Python, Poetry, Rust) will be automatically set up for you based on the `.devcontainer` configuration. The `postCreateCommand` will automatically install Python dependencies (`poetry install`) and build the Rust library (`cargo build`).

1.  **Launch Codespace:**
    Go to your [QynAuth GitHub repository](https://github.com/minkalla/qynauth), click the green `< > Code` button, select the `Codespaces` tab, and launch your Codespace.
2.  **Verify Setup (Optional):**
    Once the Codespace loads, you can verify installations in the terminal:

    ```bash
    python3 --version
    poetry --version
    cargo --version
    ```

    You should see their respective versions.
3.  **Run the FastAPI Application:**
    Navigate to the Python application directory and start the server:

    ```bash
    cd src/python_app
    poetry run uvicorn app.main:app --reload --port 3001
    ```

    You should see output indicating the server is running on `http://127.0.0.1:3001`.
4.  **Access API Documentation:**
    Open your web browser and navigate to `http://localhost:3001/docs` (or the Codespaces forwarded URL ending in `/docs`). You will see the interactive Swagger UI.

### API Endpoints

All API endpoints are documented in the Swagger UI. Here's a quick overview:

#### `POST /auth/register`

Registers a new user with a unique username and password.

* **Method:** `POST`
* **URL:** `/auth/register`
* **Request Body (JSON):**

    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```

* **Example Request (using `curl`):**

    ```bash
    curl -X POST http://localhost:3001/auth/register \
    -H "Content-Type: application/json" \
    -d '{
      "username": "mytestuser",
      "password": "MySuperStrongPassword123"
    }'
    ```

#### `POST /auth/login`

Authenticates a user and returns a JSON Web Token (JWT).

* **Method:** `POST`
* **URL:** `/auth/login`
* **Request Body (JSON):**

    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```

* **Example Request (using `curl`):**

    ```bash
    curl -X POST http://localhost:3001/auth/login \
    -H "Content-Type: application/json" \
    -d '{
      "username": "mytestuser",
      "password": "MySuperStrongPassword123"
    }'
    ```

    *The response will contain an `access_token` that you can use in `Authorization: Bearer <token>` headers for protected endpoints (future feature).*

#### `GET /health`

Checks the health of the service.

* **Method:** `GET`
* **URL:** `/health`
* **Example Request (using `curl`):**

    ```bash
    curl http://localhost:3001/health
    ```

## AuthToken Specification

For details on the JWT token structure and claims, refer to the [AuthToken Specification](docs/AUTH_TOKEN_SPEC.md).

## Running Tests

To run the unit tests for QynAuth:

```bash
cd src/python_app
poetry run pytest