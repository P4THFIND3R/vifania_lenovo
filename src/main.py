import asyncio

from src.core.service_factory import ServiceFactory

service_factory = ServiceFactory()

camera_service = service_factory.camera_service
telegram_service = service_factory.telegram_service
connection_service = service_factory.connection_service


async def main():
    await connection_service.wait_for_internet()

    await telegram_service.send_notification()

    filenames = camera_service.get_frames(1, 1)
    await telegram_service.send_photos(filenames)


if __name__ == '__main__':
    asyncio.run(main())
