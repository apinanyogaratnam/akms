import os

import uvicorn

from config import port

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=os.environ.get("ENVIRONMENT") == "development")
