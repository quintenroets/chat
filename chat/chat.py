from dataclasses import dataclass

import cli
from rich.style import Style
from rich.text import Text

from .chatmanager import ChatManager


@dataclass
class Chat:
    personal_title: Text = Text("User: ", style=Style(color="green", bold=True))
    assistant_title: Text = Text("Chatgpt: ", style=Style(color="blue", bold=True))

    def __post_init__(self):
        self.manager = ChatManager()

    def send(self, prompt: str):
        self.manager.send(prompt)
        self.show_reply()

    def show_reply(self):
        print("")
        with cli.status(""):
            self.manager.retrieve_reply()

        cli.console.print(self.assistant_title, end="")
        for chunk in self.manager.get_reply_chunks():
            print(chunk, end="")
        print("\n")
