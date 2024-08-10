from unittest.mock import MagicMock, patch

import pytest
from chat.context import Context, context
from chat.main.chat import Chat
from chat.main.history import History
from langchain_ollama import OllamaLLM


@pytest.fixture()
def test_context() -> Context:
    context.config.pause_time = 0.1
    return context


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
