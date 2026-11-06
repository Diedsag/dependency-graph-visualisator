"""
Главный модуль приложения.
Оркестрирует парсинг конфигурации и вывод результатов.
"""
import logging
import sys

from src.config import Config, parse_args
from src.fetcher import (
    BaseFetcher, NpmFetcher, TestFetcher
)
from src.graph import Graph, GraphBuilder

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)


def create_fetcher(config: Config) -> BaseFetcher:
    """Создает объект загрузчика на основе конфигурации."""
    if config.is_test_mode:
        return TestFetcher(config.source)
    return NpmFetcher(config.source)


def print_graph_summary(graph: Graph) -> None:
    """Выводит краткую сводку о построенном графе."""
    logger.info("--- Сводка по графу ---")
    logger.info(
        "Всего уникальных пакетов: %d",
        len(graph.adjacency)
    )
    for node, deps in sorted(graph.adjacency.items()):
        if deps:
            logger.info(
                "%s -> %s",
                node, ", ".join(sorted(deps))
            )
        else:
            logger.info(
                "%s -> (нет зависимостей)", node
            )
    logger.info("-----------------------")


def print_reverse_deps(
    graph: Graph, target: str
) -> None:
    """Выводит обратные зависимости для заданного пакета."""
    logger.info("--- Обратные зависимости для %s ---", target)
    reverse_deps = graph.get_reverse_dependencies(target)
    if not reverse_deps:
        logger.info("Обратные зависимости не найдены.")
    for dep in sorted(reverse_deps):
        logger.info(dep)
    logger.info("-----------------------------------")


def main() -> int:
    """Точка входа в приложение."""
    try:
        config = parse_args(sys.argv[1:])

        fetcher = create_fetcher(config)
        builder = GraphBuilder(fetcher)
        graph = builder.build(
            config.package_name, config.max_depth
        )
        print_graph_summary(graph)
        if config.reverse_for:
            print_reverse_deps(graph, config.reverse_for)

        return 0
    except ValueError as error:
        logger.error("Ошибка конфигурации: %s", error)
        return 1
    except RuntimeError as error:
        logger.error("Ошибка выполнения: %s", error)
        return 1
    except SystemExit as error:
        code = error.code
        return code if isinstance(code, int) else 1


if __name__ == "__main__":
    sys.exit(main())