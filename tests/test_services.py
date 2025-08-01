from unittest.mock import patch
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from services import handle_post, handle_get, url_mapping


class TestURLShortener(AioHTTPTestCase):
    async def get_application(self):
        """Переопределяем метод get_app, чтобы возвращать наше приложение aiohttp."""
        app = web.Application()
        app.add_routes([web.post('/', handle_post),
                        web.get('/{short_id}', handle_get)])
        return app

    async def test_handle_post(self):
        """Тестируем POST-запрос."""
        with patch("services.shorten", return_value="test_id"):  # Мокируем функцию shorten
            resp = await self.client.post('/', data="https://example.com")
            self.assertEqual(resp.status, 201)  # Проверяем статус код
            data = await resp.json()
            self.assertEqual(data['short_url'], 'test_id')  # Проверяем, что short_url вернулся корректно
            self.assertEqual(url_mapping['test_id'], "https://example.com")  # Проверяем, что URL сохранен

    async def test_handle_get_success(self):
        """Тестируем успешный GET-запрос."""
        url_mapping['test_id'] = "https://example.com"
        resp = await self.client.get('/test_id', allow_redirects=False)  # Отключаем редирект, чтобы проверить статус код
        self.assertEqual(resp.status, 302)  # Проверяем статус код редиректа
        self.assertEqual(resp.headers['Location'], "https://example.com")  # Проверяем, куда перенаправляет
        del url_mapping['test_id']  # Очищаем за собой

    async def test_handle_get_not_found(self):
        """Тестируем GET-запрос для несуществующего ID."""
        resp = await self.client.get('/nonexistent_id')
        self.assertEqual(resp.status, 404)  # Проверяем статус код "не найдено"
        text = await resp.text()
        self.assertEqual(text, "URL not found")  # Проверяем текст ответа
