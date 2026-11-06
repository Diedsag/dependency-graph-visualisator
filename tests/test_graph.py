"""Модуль тестов для построителя графа."""
from unittest.mock import MagicMock

from src.config import INFINITE_DEPTH
from src.graph import GraphBuilder


def test_graph_builder_bfs() -> None:
    """Проверяет обход в ширину."""
    mock_fetcher = MagicMock()
    mock_fetcher.fetch.side_effect = lambda pkg: {
        "A": {"B": "1", "C": "1"},
        "B": {"D": "1"},
        "C": {},
        "D": {}
    }.get(pkg, {})

    builder = GraphBuilder(mock_fetcher)
    graph = builder.build("A", INFINITE_DEPTH)

    assert graph.adjacency["A"] == {"B", "C"}
    assert graph.adjacency["B"] == {"D"}
    assert graph.adjacency["C"] == set()


def test_graph_builder_max_depth() -> None:
    """Проверяет ограничение глубины."""
    mock_fetcher = MagicMock()
    mock_fetcher.fetch.side_effect = lambda pkg: {
        "A": {"B": "1"},
        "B": {"C": "1"},
        "C": {"D": "1"},
        "D": {}
    }.get(pkg, {})

    builder = GraphBuilder(mock_fetcher)
    graph = builder.build("A", 1)

    assert "A" in graph.adjacency
    assert "B" in graph.adjacency
    assert "C" not in graph.adjacency


def test_graph_builder_cycles() -> None:
    """Проверяет корректную обработку циклов."""
    mock_fetcher = MagicMock()
    mock_fetcher.fetch.side_effect = lambda pkg: {
        "A": {"B": "1"},
        "B": {"A": "1"}
    }.get(pkg, {})

    builder = GraphBuilder(mock_fetcher)
    graph = builder.build("A", INFINITE_DEPTH)

    assert graph.adjacency["A"] == {"B"}
    assert graph.adjacency["B"] == {"A"}