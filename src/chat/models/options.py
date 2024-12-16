from dataclasses import dataclass

from .messages import Role
from .path import Path


@dataclass
class Options:
    model: str = "llama3.2"
    system_prompt: str | None = None
    conversation_starter: Role | None = None
    config_path: Path = Path.config
