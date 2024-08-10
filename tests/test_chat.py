from chat.main.chat import Chat
from chat.main.history import History


def test_chat() -> None:
    chat = Chat()
    chat.send("hi")


def test_history() -> None:
    history = History()
    history.messages.append({})
    history.close()
