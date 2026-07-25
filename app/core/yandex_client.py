# app/core/yandex_client.py
from http import HTTPStatus
from typing import AsyncGenerator, Optional, Tuple

import httpx
from fastapi import HTTPException

from app.core.config import settings

BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
REPORTS_FOLDER = 'QRKot Reports'


class YandexDiskClient:
    """Асинхронный клиент для работы с API Яндекс.Диска."""

    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': f'OAuth {token}'}
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(headers=self.headers)
        await self._create_folder()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def _create_folder(self) -> None:
        """Создаёт папку REPORTS_FOLDER на Диске, если её ещё нет."""
        response = await self.client.put(
            BASE_URL,
            params={'path': REPORTS_FOLDER},
        )
        if response.status_code == HTTPStatus.CONFLICT:
            return
        response.raise_for_status()

    async def create_excel_file(self, filename: str) -> Tuple[str, str]:
        """
        Получает ссылку для загрузки файла на Диск.

        Возвращает кортеж (upload_url, path_on_disk).
        """
        disk_path = f'{REPORTS_FOLDER}/{filename}'
        response = await self.client.get(
            f'{BASE_URL}/upload',
            params={'path': disk_path, 'overwrite': 'true'},
        )
        response.raise_for_status()
        data = response.json()
        upload_url = data.get('href')
        if not upload_url:
            raise ValueError(
                'Не удалось получить ссылку для загрузки файла на Диск.'
            )
        return upload_url, disk_path

    async def upload_file(self, upload_url: str, file_content: bytes) -> None:
        """Загружает бинарное содержимое файла по полученной ссылке."""
        response = await self.client.put(upload_url, content=file_content)
        response.raise_for_status()

    async def publish_file(self, disk_path: str) -> str:
        """Делает файл публичным и возвращает публичную ссылку на него."""
        response = await self.client.put(
            f'{BASE_URL}/publish',
            params={'path': disk_path},
        )
        response.raise_for_status()

        response = await self.client.get(
            BASE_URL,
            params={'path': disk_path},
        )
        response.raise_for_status()
        public_url = response.json().get('public_url')
        if not public_url:
            raise ValueError(
                'Не удалось получить публичную ссылку на файл.'
            )
        return public_url


async def get_yandex_client() -> AsyncGenerator[YandexDiskClient, None]:
    if not settings.yandex_disk_token:
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail='Не задан токен для работы с Яндекс.Диском.',
        )
    async with YandexDiskClient(settings.yandex_disk_token) as client:
        yield client
