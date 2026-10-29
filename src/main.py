"""
Главный модуль приложения.
Оркестрирует парсинг конфигурации и вывод результатов.
"""
import logging
import sys

from src.config import Config, parse_args
from src.fetcher import BaseFetcher, NpmFetcher, TestFetcher

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


def print_dependencies(package_name: str, deps: dict[str, str]) -> None:
    """Выводит список прямых зависимостей пакета."""
    logger.info("--- Прямые зависимости %s ---", package_name)
    if not deps:
        logger.info("Зависимости не найдены.")
    for name, version in deps.items():
        logger.info("%s: %s", name, version)
    logger.info("------------------------------")


def main() -> int:
    """Точка входа в приложение."""
    try:
        config = parse_args(sys.argv[1:])
        print_config(config)

        fetcher = create_fetcher(config)
        deps = fetcher.fetch(config.package_name)
        print_dependencies(config.package_name, deps)

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