"""
Главный модуль приложения.
Оркестрирует парсинг конфигурации и вывод результатов.
"""
import logging
import sys

from src.config import Config, parse_args
from src.fetcher import BaseFetcher, NpmFetcher, TestFetcher
from src.graph import Graph, GraphBuilder

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)


def print_config(config: Config) -> None:
    """Выводит параметры конфигурации в формате ключ-значение."""
    logger.info("--- Параметры конфигурации ---")
    logger.info("package_name: %s", config.package_name)
    logger.info("source: %s", config.source)
    logger.info("is_test_mode: %s", config.is_test_mode)
    logger.info("use_ascii_tree: %s", config.use_ascii_tree)
    logger.info("max_depth: %s", config.max_depth)
    logger.info("------------------------------")


def create_fetcher(config: Config) -> BaseFetcher:
    """Создает объект загрузчика на основе конфигурации."""
    if config.is_test_mode:
        return TestFetcher(config.source)
    return NpmFetcher(config.source)


def print_graph_summary(graph: Graph) -> None:
    """Выводит краткую сводку о построенном графе."""
    logger.info("--- Сводка по графу ---")
    logger.info("Всего уникальных пакетов: %d", len(graph.adjacency))
    for node, deps in sorted(graph.adjacency.items()):
        if deps:
            logger.info(
                "%s -> %s", node, ", ".join(sorted(deps))
            )
        else:
            logger.info("%s -> (нет зависимостей)", node)
    logger.info("-----------------------")


def main() -> int:
    """Точка входа в приложение."""
    try:
        config = parse_args(sys.argv[1:])
        print_config(config)

        fetcher = create_fetcher(config)
        builder = GraphBuilder(fetcher)
        graph = builder.build(
            config.package_name, config.max_depth
        )
        print_graph_summary(graph)

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