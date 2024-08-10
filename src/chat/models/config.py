from dataclasses import dataclass, field

from .path import Path


@dataclass
class Config:
    user_display_name: str | None = None
    assistant_display_name: str = "Assistant"
    history_path: Path = field(default_factory=Path.session.with_nonexistent_name())
