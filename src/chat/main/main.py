import cli

from chat.context.context import context

from .chat import Chat


def main() -> None:
    chat = Chat()
    while True:
        cli.console.print(context.user_title, end="")
        prompt = input()
        chat.send(prompt)
