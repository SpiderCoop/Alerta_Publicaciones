"""Shared test configuration and fixtures."""

import pytest


@pytest.fixture
def publication_row():
    """Return a representative Banxico publication row."""
    return {
        "nombre": "Consulta de prueba",
        "fecha_limite": "31/12/2026",
        "enlaces": {"Documento principal": "https://example.test/document.pdf"},
    }
