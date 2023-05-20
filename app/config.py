import os

from dotenv import load_dotenv

load_dotenv()

openapi_url = os.getenv("OPENAPI_URL", "/openapi.json")
docs_url = os.getenv("DOCS_URL", "/docs")
host = os.getenv("HOST", "localhost")
port = int(os.getenv("PORT", 8080))

reload = os.getenv("RELOAD", "True") == "True"
