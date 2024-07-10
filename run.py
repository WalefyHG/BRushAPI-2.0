import unicorn
import os
from .core import api

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    unicorn.run(api, host="0.0.0.0.", port=port)