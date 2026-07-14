from fastapi import APIRouter, Depends

from hello.version import version, build, fingerprint
from hello.auth import BasicReader, BasicWriter, BasicAdmin


router = APIRouter()
prefix = "/health"
tags = ["health"]


@router.get("")
async def get_health():
    return dict(
        status="up",
        version=version,
        build=build,
        fingerprint=fingerprint
    )


@router.get("/reader")
async def create_something(user: BasicReader):
    return await get_health()


@router.get("/writer")
async def create_something(user: BasicWriter):
    return await get_health()


@router.get("/admin")
async def create_something(user: BasicAdmin):
    return await get_health()
