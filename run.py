import os
import django
from uvicorn import run
from core.asgi import django_asgi_app
from ninja_jwt.authentication import JWTAuth


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from core.api import api

async def application(scope, receive, send):
    if scope['type'] == 'http':
        await django_asgi_app(scope, receive, send)
    else:
        await JWTAuth(api)(scope, receive, send)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    run(application, host="0.0.0.0", port=port)