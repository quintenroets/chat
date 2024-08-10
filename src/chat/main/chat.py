import time
from collections.abc import Iterator
from dataclasses import dataclass, field

import cli
from langchain_ollama import OllamaLLM

from chat.context import context
from chat.models import Message, Path, Role

from .history import History


@dataclass
class Chat:
    assistant: OllamaLLM = field(default_factory=lambda: OllamaLLM(model="llama3.1"))
    history: History = field(default_factory=lambda: History())

    def send(self, prompt: str) -> None:
        message = Message(role=Role.user, content=prompt)
        self.history.add(message)
        self.show_reply()

    def show_reply(self) -> None:
        cli.console.print(context.assistant_title, end="")
        try:
            for chunk in self.calculate_reply_chunks():
                print(chunk, end="", flush=True)  # noqa: T201
        except KeyboardInterrupt:  # pragma: nocover
            self.history.close()
        finally:
            cli.console.print("\n")

    def calculate_reply_chunks(self) -> Iterator[str]:
        response_tokens = self.assistant.stream(self.history.messages)
        chunks = []
        for chunk in response_tokens:
            if context.config.pause_time is not None:
                time.sleep(context.config.pause_time)
            chunks.append(chunk)
            yield chunk

        reply = "".join(chunks)
        message = Message(role=Role.assistant, content=reply)
        self.history.add(message)
        if context.should_copy_replies:
            self.copy_to_clipboard(reply)  # pragma: nocover

    @classmethod
    def copy_to_clipboard(cls, text: str) -> None:  # pragma: nocover
        with Path.tempfile() as tmp:
            tmp.text = text
            cli.run("xclip", tmp, "-selection", "clipboard")
