from dataclasses import dataclass

from chat.models import Path, Role


@dataclass
class Options:
    model: str = "llama3.2"
    system_prompt: str | None = None
    conversation_starter: Role | None = None
    config_path: Path = Path.config
