import time
from typing import Optional

import cv2

from src.utils.logger import logger


class CameraRepository:
    def __init__(self):
        self.camera: Optional[cv2.VideoCapture] = None

    def __enter__(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Не удалось открыть камеру.")

        return self.camera

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.camera is not None:
            self.camera.release()

    @staticmethod
    def save_img(filename: str, frame: cv2.UMat) -> bool:
        try:
            status = cv2.imwrite(filename, frame)
            logger.info(status)
            return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении изображения: {e}")
            return False

    @staticmethod
    def sleep(cooldown: int):
        logger.info(f"Пауза на {cooldown} секунд...")
        time.sleep(cooldown)
