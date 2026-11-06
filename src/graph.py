"""Модуль для построения графа зависимостей."""
from collections import deque
from dataclasses import dataclass, field

from src.config import INFINITE_DEPTH
from src.fetcher import BaseFetcher


@dataclass
class Graph:
    """Представление графа зависимостей в виде списков смежности."""
    adjacency: dict[str, set[str]] = field(default_factory=dict)

    def add_edge(self, parent: str, child: str) -> None:
        """Добавляет направленное ребро от parent к child."""
        if parent not in self.adjacency:
            self.adjacency[parent] = set()
        self.adjacency[parent].add(child)

        if child not in self.adjacency:
            self.adjacency[child] = set()

    def get_reverse_dependencies(self, target: str) -> set[str]:
        """Возвращает пакеты, которые зависят от target."""
        reverse_adj: dict[str, set[str]] = {}
        for node in self.adjacency:
            reverse_adj[node] = set()

        for parent, children in self.adjacency.items():
            for child in children:
                if child not in reverse_adj:
                    reverse_adj[child] = set()
                reverse_adj[child].add(parent)

        visited: set[str] = set()
        queue: deque[str] = deque([target])
        visited.add(target)

        while queue:
            current = queue.popleft()
            parents = reverse_adj.get(current, set())
            for parent in parents:
                if parent not in visited:
                    visited.add(parent)
                    queue.append(parent)

        visited.discard(target)
        return visited


class GraphBuilder:
    """Строит граф зависимостей алгоритмом BFS."""

    def __init__(self, fetcher: BaseFetcher) -> None:
        """Инициализирует строитель графа."""
        self.fetcher = fetcher

    def build(
            self,
            start_package: str,
            max_depth: int
    ) -> Graph:
        """Строит граф от стартового пакета с учетом глубины и циклов."""
        graph = Graph()
        visited: set[str] = set()

        queue: deque[tuple[str, int]] = deque()
        queue.append((start_package, 0))
        visited.add(start_package)

        while queue:
            current_pkg, depth = queue.popleft()

            if max_depth != INFINITE_DEPTH and depth >= max_depth:
                continue

            try:
                deps = self.fetcher.fetch(current_pkg)
            except RuntimeError:
                continue

            for dep_name in deps:
                graph.add_edge(current_pkg, dep_name)

                if dep_name not in visited:
                    visited.add(dep_name)
                    queue.append((dep_name, depth + 1))

        return graph