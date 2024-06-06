# -*- coding:utf-8 -*-
from fastapi import APIRouter
from app.api.endpoints import spider_notify


api_router = APIRouter()
api_router.include_router(spider_notify.router,
                          prefix="/tali", tags=["tali"])
