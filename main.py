import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = os.environ.get("PORT")

    try:
        port = int(port)
    except ValueError as e:
        raise EnvironmentError(f"Invalid port {port} from environment") from e

    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=os.environ.get("ENVIRONMENT") == "development")
