import os
from functools import cached_property

import cli
from package_utils.context import Context as Context_
from rich.style import Style
from rich.text import Text

from chat.models import Config, Options


class Context(Context_[Options, Config, None]):
    @cached_property
    def user_header(self) -> str:
        name = (
            self.extract_username()
            if self.config.user_display_name is None
            else self.config.user_display_name
        )
        return f"{name}: "

    @cached_property
    def assistant_header(self) -> str:
        return f"{self.config.assistant_display_name}: "

    @cached_property
    def should_copy_replies(self) -> bool:
        return self.can_copy_text()

    @classmethod
    def extract_username(cls) -> str:
        try:
            username = os.getlogin().capitalize()
        except OSError:  # pragma: nocover
            username = "User"
        return username

    @classmethod
    def can_copy_text(cls) -> bool:
        required_programs = ("echo", "xclip")
        return all(
            cli.completes_successfully(f"which {program}")
            for program in required_programs
        )

    @cached_property
    def user_title(self) -> Text:
        return Text(context.user_header, style=Style(color="green", bold=True))

    @cached_property
    def assistant_title(self) -> Text:
        return Text(context.assistant_header, style=Style(color="blue", bold=True))


context = Context(Options, Config, None)
