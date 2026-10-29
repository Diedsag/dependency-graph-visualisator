"""Модуль тестов для проверки парсинга и валидации конфигурации."""
import pytest

from src.config import INFINITE_DEPTH, parse_args

EXPECTED_DEPTH = 2
INVALID_DEPTH = -2


def test_parse_args_success() -> None:
    """Проверяет успешный парсинг валидных аргументов."""
    args = [
        "--package", "express",
        "--source", "http://test.com",
        "--max-depth", str(EXPECTED_DEPTH)
    ]
    config = parse_args(args)
    assert config.package_name == "express"
    assert config.max_depth == EXPECTED_DEPTH
    assert not config.is_test_mode


def test_parse_args_default_depth() -> None:
    """Проверяет значение глубины по умолчанию."""
    args = ["--package", "lodash", "--source", "https://test.com"]
    config = parse_args(args)
    assert config.max_depth == INFINITE_DEPTH


def test_parse_args_invalid_depth() -> None:
    """Проверяет обработку некорректной глубины."""
    args = [
        "--package", "pkg",
        "--source", "https://src.com",
        "--max-depth", str(INVALID_DEPTH)
    ]
    with pytest.raises(ValueError):
        parse_args(args)


def test_parse_args_invalid_package_name() -> None:
    """Проверяет обработку некорректного имени пакета (Regex)."""
    args = [
        "--package", "INVALID NAME!",
        "--source", "https://test.com"
    ]
    with pytest.raises(ValueError):
        parse_args(args)


def test_parse_args_empty_package_name() -> None:
    """Проверяет обработку пустого имени пакета."""
    args = [
        "--package", "",
        "--source", "https://test.com"
    ]
    with pytest.raises(ValueError):
        parse_args(args)


def test_parse_args_invalid_url() -> None:
    """Проверяет обработку некорректного URL (Regex)."""
    args = [
        "--package", "express",
        "--source", "not-a-valid-url"
    ]
    with pytest.raises(ValueError):
        parse_args(args)


def test_parse_args_test_mode_allows_file_path() -> None:
    """Проверяет, что в test-mode источник проверяется как путь."""
    args = [
        "--package", "A",
        "--source", "local/path.json",
        "--test-mode"
    ]
    config = parse_args(args)
    assert config.source == "local/path.json"


def test_parse_args_test_mode_rejects_bad_path() -> None:
    """Проверяет, что в test-mode отклоняется путь без расширения."""
    args = [
        "--package", "A",
        "--source", "noextension",
        "--test-mode"
    ]
    with pytest.raises(ValueError):
        parse_args(args)