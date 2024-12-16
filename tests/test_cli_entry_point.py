from unittest.mock import MagicMock, patch

import pytest
from package_dev_utils.tests.args import no_cli_args

from chat import cli


@patch("builtins.input", return_value="")
@patch("chat.main.chat.Chat.send", side_effect=KeyboardInterrupt)
@pytest.mark.usefixtures("test_context")
@no_cli_args
def test_cli_entry_point(mocked_input: MagicMock, mocked_send: MagicMock) -> None:
    with pytest.raises(KeyboardInterrupt):
        cli.entry_point()
    mocked_input.assert_called_once()
    mocked_send.assert_called_once()
