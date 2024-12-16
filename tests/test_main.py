from unittest.mock import MagicMock, patch

import pytest

from chat.main.main import main


@patch("builtins.input", return_value="")
@patch("chat.main.chat.Chat.send", side_effect=KeyboardInterrupt)
@patch("chat.main.chat.Chat.show_reply")
@pytest.mark.usefixtures("test_context")
def test_main(
    mocked_input: MagicMock,
    mocked_send: MagicMock,
    mocked_reply: MagicMock,
) -> None:
    with pytest.raises(KeyboardInterrupt):
        main()
    mocked_input.assert_called_once()
    mocked_reply.assert_called_once()
    mocked_send.assert_called_once()
