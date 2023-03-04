import os
from dataclasses import asdict, dataclass, field
from enum import Enum
from functools import cached_property

import cli
import requests

API_URL = "https://api.openai.com/v1/chat/completions"


class Role(Enum):
    user = "user"
    assistant = "assistant"


@dataclass
class Message:
    role: Role
    content: str

    def serialize(self):
        return {"role": self.role.value, "content": self.content}


@dataclass
class Messages:
    messages: list[Message] = field(default_factory=list)

    def serialize(self):
        return [message.serialize() for message in self.messages]

    def append(self, message: Message):
        self.messages.append(message)


@dataclass
class Data:
    messages: Messages
    model: str = "gpt-3.5-turbo"
    temperature: float = 1
    top_p: float = 1
    n: int = 1
    stream: bool = True

    def serialize(self):
        items = asdict(self)
        items["messages"] = self.messages.serialize()
        return items


@dataclass
class API:
    url: str = "https://api.openai.com/v1/chat/completions"

    def __post_init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}",
        }

    def get_reply(self, messages: Messages):
        data = Data(messages).serialize()
        return requests.post(
            self.url, headers=self.headers, json=data, timeout=30, stream=True
        )

    @cached_property
    def key(self) -> str:
        try:
            key = cli.get("pw OPENAI_API_KEY")
        except FileNotFoundError:
            key = os.environ.get("OPENAI_API_KEY")
        if key is None:
            key = cli.prompt("OpenAI API key: ")
        return key
