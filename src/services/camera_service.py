import os.path
from typing import Optional
from datetime import datetime

from src.utils.logger import logger
from src.repositories.camera_repository import CameraRepository


class CameraService:
    def __init__(self, repository: CameraRepository):
        self.repository = repository
        self._directory: str = 'photos'

    def get_frame(self, filename: str = None) -> Optional[os.path]:
        if not filename:
            filename = self._create_filename()

        with self.repository as camera:
            ret, frame = camera.read()
            if not ret:
                logger.error("Failed to capture frame from camera")
                return None

            status = self.repository.save_img(filename, frame)
            if not status:
                logger.error("Failed to save frame to disk")
                return None

        return os.path.abspath(filename)

    def get_frames(self, count: int = 3, cooldown: int = 60) -> list[os.path]:
        frames = []

        for _ in range(count):
            filename = self.get_frame()
            if filename:
                frames.append(filename)
                logger.info(f"Captured frame: {filename}")
                self.repository.sleep(cooldown)
            else:
                logger.warning(f"Failed to capture frame, breaking loop. Count: {_}")
                break

        return frames

    def _create_filename(self) -> str:
        self._prepare_directory()

        return os.path.join(self._directory, datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.jpg')

    def _prepare_directory(self) -> None:
        if not os.path.exists(self._directory):
            logger.info(f"Creating directory: {self._directory}")
            os.makedirs(self._directory)
