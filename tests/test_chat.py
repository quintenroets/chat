from unittest.mock import MagicMock, patch

import pytest
from langchain_ollama import OllamaLLM

from chat.main.chat import Chat
from chat.main.history import History


@patch.object(OllamaLLM, "__init__", return_value=None)
@patch.object(OllamaLLM, "stream", return_value=["hello", "world"])
@pytest.mark.usefixtures("test_context")
def test_chat(mocked_llm: MagicMock, mocked_stream: MagicMock) -> None:
    chat = Chat()
    chat.send("hi")
    mocked_llm.assert_called_once()
    mocked_stream.assert_called_once()


def test_history() -> None:
    history = History()
    history.messages.append({})
    history.close()
