
from fastapi import APIRouter
from fastapi import Body
from typing import List, Tuple
from app.service.spider_notify import spider_notify
from sse_starlette import EventSourceResponse
# from app.utils.history import History

router = APIRouter()


@router.post("/spider_notify")
async def api_spider_notify(message: str = Body(..., description="用户输入", examples=["你好"]),
                            history: list[list[str | tuple | None]] = Body([], description="历史记录")):

    # 创建一个 sse 响应
    return EventSourceResponse(spider_notify.extra_info(message, history))
