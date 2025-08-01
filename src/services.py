from aiohttp import web
import hashlib

url_mapping = {}


def shorten(url):
    encoded_url = url.encode()
    hash_object = hashlib.md5(encoded_url)
    return hash_object.hexdigest()[:8]


async def handle_post(request):
    """Обработчик POST-запросов."""
    data = await request.text()
    original_url = data
    short_id = shorten(original_url)
    url_mapping[short_id] = original_url
    return web.json_response({'short_url': short_id}, status=201)


async def handle_get(request):
    """Обработчик GET-запросов."""
    short_id = request.match_info['short_id']
    if short_id in url_mapping:
        return web.HTTPFound(url_mapping[short_id])
    else:
        return web.Response(text="URL not found", status=404)
