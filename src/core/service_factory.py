from typing import Optional

from src.core.config import settings
from src.services.camera_service import CameraService
from src.repositories.camera_repository import CameraRepository
from src.services.telegram_service import TelegramService


class ServiceFactory:
    def __init__(self):
        self._camera_repository: Optional[CameraRepository] = None
        self._camera_service: Optional[CameraService] = None

        self._telegram_service: Optional[TelegramService] = None

    @property
    def camera_repository(self) -> CameraRepository:
        if not self._camera_repository:
            self._camera_repository = CameraRepository()
        return self._camera_repository

    @property
    def camera_service(self) -> CameraService:
        if not self._camera_service:
            self._camera_service = CameraService(self.camera_repository)
        return self._camera_service

    @property
    def telegram_service(self) -> TelegramService:
        if not self._telegram_service:
            self._telegram_service = TelegramService(
                api_token=settings.BOT_TOKEN,
                chat_id=settings.CHAT_ID
            )
        return self._telegram_service
