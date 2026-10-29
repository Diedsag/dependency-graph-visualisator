"""Модуль тестов для проверки логики получения зависимостей."""
import json
from unittest.mock import MagicMock, patch

from src.fetcher import NpmFetcher


def test_npm_fetcher_success() -> None:
    """Проверяет успешное извлечение зависимостей из npm."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "dependencies": {"lodash": "^4.17.21"}
    }).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        fetcher = NpmFetcher("https://registry.npmjs.org")
        deps = fetcher.fetch("express")

    assert deps == {"lodash": "^4.17.21"}


def test_npm_fetcher_no_deps() -> None:
    """Проверяет пакет без зависимостей."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({}).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        fetcher = NpmFetcher("https://registry.npmjs.org")
        deps = fetcher.fetch("some-empty-pkg")

    assert deps == {}