import cli

from .chat import Chat


def main():
    chat = Chat()
    while True:
        cli.console.print(chat.personal_title, end="")
        prompt = input()
        chat.send(prompt)
