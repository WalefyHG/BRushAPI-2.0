import uvicorn
import os
from core.api import api

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(api, host="0.0.0.0", port=port, reload=True)