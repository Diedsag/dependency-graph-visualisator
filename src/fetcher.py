"""Модуль для получения данных о зависимостях пакетов."""
import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod

USER_AGENT = "DependencyGraphVisualizer/1.0"


class BaseFetcher(ABC):
    """Абстрактный базовый класс для получения зависимостей."""

    @abstractmethod
    def fetch(self, package_name: str) -> dict[str, str]:
        """Возвращает словарь прямых зависимостей."""
        ...


class NpmFetcher(BaseFetcher):
    """Получает зависимости из реестра npm."""

    def __init__(self, base_url: str) -> None:
        """Инициализирует загрузчик базовым URL."""
        self.base_url = base_url.rstrip("/")

    def fetch(self, package_name: str) -> dict[str, str]:
        """Запрашивает данные пакета и извлекает зависимости."""
        url = f"{self.base_url}/{package_name}/latest"
        req = urllib.request.Request(
            url, headers={"User-Agent": USER_AGENT}
        )
        try:
            with urllib.request.urlopen(req) as response:
                raw_data = response.read().decode("utf-8")
                data = json.loads(raw_data)
            return data.get("dependencies", {})
        except urllib.error.HTTPError as error:
            raise RuntimeError(f"Ошибка HTTP: {error.code}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"Ошибка сети: {error}") from error


class TestFetcher(BaseFetcher):
    """Загружает тестовые зависимости из локального файла."""

    def __init__(self, file_path: str) -> None:
        """Инициализирует тестовый загрузчик путем к файлу."""
        self.file_path = file_path

    def fetch(self, package_name: str) -> dict[str, str]:
        """Читает тестовый файл и возвращает зависимости."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data.get(package_name, {}).get("dependencies", {})
        except FileNotFoundError as error:
            raise RuntimeError(f"Файл не найден: {error}") from error