import cli

from chat.context.context import context
from chat.models import Role

from .chat import Chat


def main() -> None:
    chat = Chat()
    if context.conversation_starter == Role.assistant:
        chat.show_reply()
    while True:
        cli.console.print(context.user_title, end="")
        prompt = input()
        chat.send(prompt)
