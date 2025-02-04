import asyncio

from src.core.service_factory import ServiceFactory

service_factory = ServiceFactory()

camera_service = service_factory.camera_service
telegram_service = service_factory.telegram_service


async def main():
    await telegram_service.send_notification()

    filenames = camera_service.get_frames(1, 1)
    await telegram_service.send_photos(filenames)


if __name__ == '__main__':
    asyncio.run(main())
