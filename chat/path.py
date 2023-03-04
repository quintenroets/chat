import plib

root = plib.Path(__file__).parent


class Path(plib.Path):
    assets: plib.Path = plib.Path.assets / root.name
    history = assets / "history"
    session = history / "session"
