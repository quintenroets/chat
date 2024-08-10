from collections.abc import Iterator
from dataclasses import dataclass, field

import cli
from langchain_ollama import OllamaLLM

from chat.context import context
from chat.models import Message, Path, Role


@dataclass
class Chat:
    assistant: OllamaLLM = field(default_factory=lambda: OllamaLLM(model="llama3.1"))

    def send(self, prompt: str) -> None:
        message = Message(role=Role.user, content=prompt)
        context.history.add(message)
        self.show_reply()

    def show_reply(self) -> None:
        cli.console.print(context.assistant_title, end="")
        try:
            for chunk in self.calculate_reply_chunks():
                print(chunk, end="", flush=True)  # noqa: T201
        except KeyboardInterrupt:
            context.history.close()
        finally:
            cli.console.print("\n")

    def calculate_reply_chunks(self) -> Iterator[str]:
        response_tokens = self.assistant.stream(context.history.messages)
        chunks = []
        for chunk in response_tokens:
            chunks.append(chunk)
            yield chunk

        reply = "".join(chunks)
        message = Message(role=Role.assistant, content=reply)
        context.history.add(message)
        if context.should_copy_replies:
            self.copy_to_clipboard(reply)

    @classmethod
    def copy_to_clipboard(cls, text: str) -> None:
        with Path.tempfile() as tmp:
            tmp.text = text
            cli.run("xclip", tmp, "-selection", "clipboard")
