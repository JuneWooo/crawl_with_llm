import asyncio
from typing import Optional, Awaitable
from loguru import logger


log_verbose = False


def get_prompt_template(type: str, name: str) -> Optional[str]:
    '''
    从prompt_config中加载模板内容
    type: "llm_chat","agent_chat","knowledge_base_chat","search_engine_chat"的其中一种，如果有新功能，应该进行加入。
    '''

    from app.config import prompt_config
    import importlib
    importlib.reload(prompt_config)
    return prompt_config.PROMPT_TEMPLATES[type].get(name)


async def wrap_done(fn: Awaitable, event: asyncio.Event):
    """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
    try:
        await fn
    except Exception as e:
        msg = f"Caught exception: {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
    finally:
        # Signal the aiter to stop.
        event.set()
