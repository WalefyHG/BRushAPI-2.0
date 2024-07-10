import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

import uvicorn
from core.api import api 

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(api, host="0.0.0.0", port=port)