"""Kivy application bootstrap for the tabletop click-dummy UI."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder

from tabletop.tabletop_view import TabletopRoot

Config.set("graphics", "multisamples", "0")
Config.set("graphics", "maxfps", "60")
Config.set("graphics", "vsync", "1")
Config.set("kivy", "exit_on_escape", "0")
Config.write()

_KV_LOADED = False


class TabletopApp(App):
    def __init__(
        self,
        *,
        session: Optional[int] = None,
        block: Optional[int] = None,
        player: str = "VP1",
        **kwargs: Any,
    ) -> None:
        self._session = session
        self._block = block
        self._player = player
        super().__init__(**kwargs)

    def build(self) -> TabletopRoot:
        global _KV_LOADED
        if not _KV_LOADED:
            Builder.load_file(str(Path(__file__).parent / "ui" / "layout.kv"))
            _KV_LOADED = True
        return TabletopRoot(
            bridge=None,
            bridge_player=self._player,
            bridge_session=self._session,
            bridge_block=self._block,
            single_block_mode=True,
            perf_logging=False,
        )


def main(*, session: Optional[int] = 1, block: Optional[int] = 1, player: str = "VP1") -> None:
    TabletopApp(session=session, block=block, player=player).run()


def app_main() -> None:
    """Launch the conference click-dummy with fixed defaults."""

    main(session=1, block=1, player="VP1")


if __name__ == "__main__":
    app_main()
