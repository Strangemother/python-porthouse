
import asyncio
import uvicorn
from fastapi import FastAPI
from pathlib import Path

import config as conf

HERE = Path(__file__).parent.as_posix()


async def main():
    """
    python -m uvicorn ingress:app --host 127.0.0.1 --port 9004  --reload
    """
    config = uvicorn.Config("ingress:app",
            host=conf.HOST,
            port=conf.PORT,
            log_level="info",
            reload=True,
            reload_dirs=[HERE],
            )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())

