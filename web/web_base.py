from pydantic import Field
from gradio.data_classes import GradioModel, FileData
from typing import Literal, Optional, List


class ThoughtMetadata(GradioModel):
    tool_name: Optional[str] = None
    error: bool = False


class ChatMessage(GradioModel):
    role: Literal["user", "assistant"]
    content: str
    thought_metadata: ThoughtMetadata = Field(default_factory=ThoughtMetadata)


class ChatFileMessage(GradioModel):
    role: Literal["user", "assistant"]
    file: FileData
    thought_metadata: ThoughtMetadata = Field(default_factory=ThoughtMetadata)
    alt_text: Optional[str] = None


def chat_echo(prompt: str, messages: List[ChatMessage | ChatFileMessage]) -> List[ChatMessage | ChatFileMessage]:
    messages.append(ChatMessage(role="user", content=prompt))
    messages.append(ChatMessage(role="assistant", content=prompt))
    return messages
