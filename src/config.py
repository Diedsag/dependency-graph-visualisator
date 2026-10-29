"""
Модуль для парсинга аргументов командной строки и валидации конфигурации.
"""
import argparse
import re
from dataclasses import dataclass

INFINITE_DEPTH = -1
MIN_VALID_DEPTH = -1
PACKAGE_NAME_PATTERN = re.compile(r"^[a-z0-9@\/._-]+$", re.IGNORECASE)
URL_PATTERN = re.compile(r"^https?:\/\/.*")
FILE_PATH_PATTERN = re.compile(r"^.+\..+$")


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


def _validate_package_name(name: str) -> None:
    """Проверяет имя пакета на соответствие формату через Regex."""
    if not name:
        raise ValueError("Имя пакета не может быть пустым.")
    if not PACKAGE_NAME_PATTERN.match(name):
        raise ValueError(
            f"Некорректное имя пакета: '{name}'."
        )


def _validate_source(source: str, is_test_mode: bool) -> None:
    """Проверяет источник (URL репозитория или путь к файлу)."""
    if not source:
        raise ValueError("Источник не может быть пустым.")
    if is_test_mode:
        if not FILE_PATH_PATTERN.match(source):
            raise ValueError(
                f"Некорректный путь к файлу: '{source}'."
            )
    else:
        if not URL_PATTERN.match(source):
            raise ValueError(
                f"Некорректный URL репозитория: '{source}'."
            )


def _validate_depth(depth: int) -> None:
    """Проверяет значение глубины анализа."""
    if depth < MIN_VALID_DEPTH:
        raise ValueError(
            f"Глубина должна быть >= {MIN_VALID_DEPTH}."
        )


def parse_args(args: list[str]) -> Config:
    """
    Парсит аргументы и возвращает объект Config.
    Выбрасывает ValueError при некорректных параметрах.
    """
    parser = _build_parser()
    parsed = parser.parse_args(args)

    _validate_package_name(parsed.package)
    _validate_source(parsed.source, parsed.test_mode)
    _validate_depth(parsed.max_depth)

    return Config(
        package_name=parsed.package,
        source=parsed.source,
        is_test_mode=parsed.test_mode,
        use_ascii_tree=parsed.ascii_tree,
        max_depth=parsed.max_depth
    )