"""
Configuração do Pytest.
"""

import os
import sys

import pytest

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(scope="session")
def app():
    """Create application for the tests."""
    # Configurar variáveis de ambiente antes de importar
    os.environ["USE_DATABASE"] = "False"
    os.environ["USE_REDIS"] = "False"
    os.environ["TESTING"] = "True"

    from src import create_app

    app = create_app("development")
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    print("✓ App de teste criada (JSON mode, Cache desabilitado)")

    yield app


@pytest.fixture(scope="session")
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def auth_headers(client):
    """Get authentication headers for protected routes."""
    # Login como admin
    response = client.post("/auth/login", json={"email": "admin@angodata.ao", "password": "admin123"})

    if response.status_code == 200:
        data = response.get_json()
        token = data.get("access_token")
        return {"Authorization": f"Bearer {token}"}

    return {}


@pytest.fixture(scope="function")
def editor_headers(client):
    """Get authentication headers for editor role."""
    response = client.post("/auth/login", json={"email": "editor@angodata.ao", "password": "editor123"})

    if response.status_code == 200:
        data = response.get_json()
        token = data.get("access_token")
        return {"Authorization": f"Bearer {token}"}

    return {}


@pytest.fixture(scope="session")
def db_app():
    """Create application with database for integration tests."""
    os.environ["USE_DATABASE"] = "True"
    os.environ["USE_REDIS"] = "False"
    os.environ["TESTING"] = "True"

    # Se DATABASE_URL não estiver configurado, skip tests de database
    if not os.getenv("DATABASE_URL") or "YOUR_PASSWORD_HERE" in os.getenv("DATABASE_URL"):
        pytest.skip("Database não configurado")

    app = create_app("development")
    app.config["TESTING"] = True

    # Inicializar database
    init_database()

    yield app

    # Cleanup não é necessário pois usamos database real


@pytest.fixture(scope="function")
def db_client(db_app):
    """Create a test client with database."""
    return db_app.test_client()
