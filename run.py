import os
import django
from core.api import api

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import uvicorn

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(api, host="0.0.0.0", port=port)