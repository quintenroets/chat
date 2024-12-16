from dataclasses import dataclass
from enum import Enum


class Role(Enum):
    assistant = "assistant"
    system = "system"
    user = "user"


@dataclass
class Message:
    role: Role
    content: str

    def serialize(self) -> dict[str, str]:
        return {"role": self.role.value, "content": self.content}
