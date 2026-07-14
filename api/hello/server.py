import logging

import uvicorn
from fastapi import FastAPI, APIRouter

from hello.config import config, project
from hello.services import services


log = logging.getLogger(__name__)


class Server:

    def __init__(self):
        self.prefix = config.getstr('server.prefix', '/api/p')
        self.app = FastAPI(
            title=project['name'],
            version=project['version'],
            description=project['description'],
            docs_url=f'{self.prefix}/docs',
            redoc_url=f'{self.prefix}/redoc',
            openapi_url=f'{self.prefix}/openapi.json',
        )
        router = APIRouter()
        for service in services:
            router.include_router(service.router, prefix=service.prefix, tags=service.tags)
        self.app.include_router(router, prefix=self.prefix)

        log.debug(f"Server initialized with prefix: {self.prefix}")

    def run(self):
        host = config.getstr('server.host', '0.0.0.0')
        port = config.getint('server.port', 8000)
        uvicorn.run(self.app, host=host, port=port, log_config=None, proxy_headers=True)
