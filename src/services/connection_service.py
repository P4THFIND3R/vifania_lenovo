import asyncio
import aiohttp

from src.utils.logger import logger


class ConnectionService:
    async def wait_for_internet(self, timeout: int = 1800, check_interval: int = 30):
        start_time = asyncio.get_event_loop().time()

        while True:
            if await self._is_internet_available():
                logger.info("Интернет доступен, продолжаем выполнение")
                return

            elapsed_time = asyncio.get_event_loop().time() - start_time
            if elapsed_time > timeout:
                raise TimeoutError("Время ожидания интернета истекло")

            logger.warning(f"Интернет недоступен, пробуем снова через {check_interval} секунд...")
            await asyncio.sleep(check_interval)

    @staticmethod
    async def _is_internet_available(timeout=5) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com", timeout=timeout) as response:
                    return response.status == 200
        except Exception as e:
            return False
