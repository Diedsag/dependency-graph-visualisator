"""Модуль тестов для проверки парсинга конфигурации."""
import pytest

from src.config import INFINITE_DEPTH, parse_args


def test_parse_args_success() -> None:
    """Проверяет успешный парсинг валидных аргументов."""
    args = [
        "--package", "express",
        "--source", "http://test.com",
        "--max-depth", "2"
    ]
    config = parse_args(args)
    assert config.package_name == "express"
    assert config.max_depth == 2
    assert not config.is_test_mode


def test_parse_args_default_depth() -> None:
    """Проверяет значение глубины по умолчанию."""
    args = ["--package", "lodash", "--source", "test"]
    config = parse_args(args)
    assert config.max_depth == INFINITE_DEPTH


def test_parse_args_invalid_depth() -> None:
    """Проверяет обработку некорректной глубины."""
    args = [
        "--package", "pkg",
        "--source", "src",
        "--max-depth", "-2"
    ]
    with pytest.raises(ValueError):
        parse_args(args)