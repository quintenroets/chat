from typing import TypeVar, cast

import superpathlib
from simple_classproperty import classproperty
from typing_extensions import Self

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
    @classmethod
    @classproperty
    def source_root(cls) -> Self:
        return cls(__file__).parent.parent

    @classmethod
    @classproperty
    def assets(cls) -> Self:
        path = cls.script_assets / cls.source_root.name
        return cast("Self", path)

    @classmethod
    @classproperty
    def config(cls) -> Self:
        path = cls.assets / "config" / "config.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def history(cls: type[T]) -> T:
        path = cls.assets / "history"
        return cast(T, path)

    @classmethod
    @classproperty
    def session(cls: type[T]) -> T:
        path = cls.history / "session"
        return cast("Self", path)
