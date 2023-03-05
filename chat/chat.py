from dataclasses import dataclass

import cli
from rich.style import Style
from rich.text import Text

from .chatmanager import ChatManager


@dataclass
class Chat:
    def __post_init__(self):
        self.manager = ChatManager()
        self.personal_title = Text(
            self.manager.user_title_text, style=Style(color="green", bold=True)
        )
        self.assistant_title = Text(
            self.manager.chatbot_title_text, style=Style(color="blue", bold=True)
        )

    def send(self, prompt: str):
        self.manager.send(prompt)
        self.show_reply()

    def show_reply(self):
        print("")
        with cli.status(""):
            self.manager.retrieve_reply()

        cli.console.print(self.assistant_title, end="")

        try:
            for chunk in self.manager.get_reply_chunks():
                print(chunk, end="", flush=True)
        except KeyboardInterrupt:
            self.manager.messages.messages.pop(-1)
        finally:
            print("\n")
