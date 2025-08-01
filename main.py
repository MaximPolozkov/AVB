import asyncio
import signal

from aiohttp import web
from services import handle_post, handle_get


async def main():
    """Главная функция для запуска сервера."""
    app = web.Application()
    app.add_routes([
        web.post('/', handle_post),
        web.get('/{short_id}', handle_get)
    ])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()
    print("Сервер запущен на порту 8080")
    await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
