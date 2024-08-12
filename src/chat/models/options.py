from dataclasses import dataclass

from .path import Path


@dataclass
class Options:
    config_path: Path = Path.config
    model: str = "llama3.1"
