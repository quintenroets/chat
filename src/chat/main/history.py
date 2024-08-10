from dataclasses import dataclass, field

from chat.context.context import context
from chat.models import Message, Role


@dataclass
class History:
    messages: list[dict[str, str]] = field(default_factory=list)

    def add(self, message: Message) -> None:
        serialized_message = message.serialize()
        self.messages.append(serialized_message)
        self.save(message)

    @classmethod
    def save(cls, message: Message) -> None:
        header = (
            context.assistant_header
            if message.role == Role.assistant
            else context.user_header
        )
        message_parts = (header, message.content, "\n" * 2)
        content = "".join(message_parts)
        with context.config.history_path.open("a") as fp:
            fp.write(content)

    def close(self) -> None:
        self.messages.pop(-1)
