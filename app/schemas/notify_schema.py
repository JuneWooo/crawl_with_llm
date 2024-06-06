from typing import Optional

from pydantic import BaseModel


class TextString(BaseModel):
    title: Optional[str]
    content: Optional[str]