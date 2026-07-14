from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from hello.version import banner


router = APIRouter()
prefix = "/banner"
tags = ["banner"]


@router.get("")
async def get_banner():
    return PlainTextResponse(banner)
