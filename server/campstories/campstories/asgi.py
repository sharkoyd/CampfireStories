# asgi.py

import os
import asyncio
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campstories.settings')
django_application = get_asgi_application()

async def application(scope, receive, send):
    await django_application(scope, receive, send)

# Optional: If you want to use Celery for background task processing, configure the Celery app here

