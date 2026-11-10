import os
import pytest

# Set ALLOW_SIMULATION=true specifically for pytest suites
os.environ["ALLOW_SIMULATION"] = "true"
os.environ["DEBUG"] = "false"
os.environ["DISCORD_ENABLED"] = "false"
os.environ["WEBHOOK_URL"] = ""


@pytest.fixture(autouse=True)
def offline_services(monkeypatch):
    """Tests never contact the configured production DB, Indexer or Discord."""
    from app import database
    from app import main
    from app.services import wazuh_service
    monkeypatch.setattr(database, "get_db", lambda: None)
    monkeypatch.setattr(wazuh_service, "query_indexer", lambda *args, **kwargs: None)
    monkeypatch.setattr(main, "test_postgres_connection", lambda: True)
    monkeypatch.setattr(main, "get_vertex_client", lambda: None)
