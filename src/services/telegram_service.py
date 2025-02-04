import asyncio
from datetime import datetime

import geocoder
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from telegram import InputMediaPhoto, InputFile

from src.utils.logger import logger


class TelegramService:
    def __init__(self, api_token: str, chat_id: str):
        self._CHAT_ID = chat_id

        self.bot = Bot(token=api_token)
        self.dp = Dispatcher(bot=self.bot)

    async def close(self):
        await self.bot.close()
        logger.info("Telegram bot closed.")

    async def send_notification(self):
        g = geocoder.ip('me')
        message = f"Ноутбук запущен! Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}. Широта и долгота: {g.latlng}"
        await self.bot.send_message(chat_id=self._CHAT_ID, text=message)

    async def send_photos(self, photos: list[str]):
        tasks = [asyncio.create_task(self._send_photo_task(photo)) for photo in photos]
        result = await asyncio.gather(*tasks)

    async def _send_photo_task(self, photo_url: str):
        try:
            photo = FSInputFile(path=photo_url)
            await self.bot.send_photo(chat_id=self._CHAT_ID, photo=photo)
        except Exception as e:
            logger.error(e.__str__())
            await self.bot.send_message(chat_id=self._CHAT_ID, text=e.__str__())
            raise
