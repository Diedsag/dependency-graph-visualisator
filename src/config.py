"""
Модуль для парсинга аргументов командной строки и валидации конфигурации.
"""
import argparse
from dataclasses import dataclass

INFINITE_DEPTH = -1
MIN_VALID_DEPTH = -1


@dataclass(frozen=True)
class Config:
    """
    Класс конфигурации приложения.
    Хранит валидированные параметры, полученные от пользователя.
    """
    package_name: str
    source: str
    is_test_mode: bool
    use_ascii_tree: bool
    max_depth: int


def _build_parser() -> argparse.ArgumentParser:
    """Создает и настраивает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей."
    )
    parser.add_argument(
        "--package",
        type=str,
        required=True,
        help="Имя анализируемого пакета."
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="URL репозитория или путь к тестовому файлу."
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Режим работы с тестовым репозиторием."
    )
    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Вывод зависимостей в формате ASCII-дерева."
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=INFINITE_DEPTH,
        help="Максимальная глубина анализа."
    )
    return parser


def parse_args(args: list[str]) -> Config:
    """
    Парсит аргументы и возвращает объект Config.
    Выбрасывает ValueError при некорректной глубине.
    """
    parser = _build_parser()
    parsed = parser.parse_args(args)

    if parsed.max_depth < MIN_VALID_DEPTH:
        raise ValueError(
            f"Глубина должна быть >= {MIN_VALID_DEPTH}."
        )

    return Config(
        package_name=parsed.package,
        source=parsed.source,
        is_test_mode=parsed.test_mode,
        use_ascii_tree=parsed.ascii_tree,
        max_depth=parsed.max_depth
    )