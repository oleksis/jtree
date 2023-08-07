from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer, Header

from jtree.widgets import JSONDocument, JSONDocumentView, JSONTree, TreeView

if TYPE_CHECKING:
    from io import TextIOWrapper

__prog_name__ = "jtree"
__version__ = "0.2.5"


class JSONTreeApp(App):
    TITLE = __prog_name__
    SUB_TITLE = f"A JSON Tree Viewer ({__version__})"
    CSS_PATH = "css/layout.css"

    BINDINGS = [
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("ctrl+t", "toggle_root", "Toggle root"),
        Binding("ctrl+q", "app.quit", "Quit"),
    ]

    def __init__(
        self,
        json_file: TextIOWrapper,
        driver_class=None,
        css_path=None,
        watch_css=False,
    ):
        super().__init__(driver_class, css_path, watch_css)
        self.json_data: str = ""

        if json_file is sys.stdin:
            self.json_data = "".join(sys.stdin.readlines())
        else:
            self.json_data = json_file.read()
            json_file.close()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            TreeView(id="tree-view"), JSONDocumentView(id="json-docview"), id="app-grid"
        )
        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one(JSONTree)
        root_name = "JSON"
        json_node = tree.root.add(root_name)
        json_data = json.loads(self.json_data)
        tree.add_node(root_name, json_node, json_data)
        json_doc = self.query_one(JSONDocument)
        json_doc.load(self.json_data)

    def action_screenshot(self):
        self.save_screenshot("./json-tree.svg")

    def action_toggle_root(self) -> None:
        tree = self.query_one(JSONTree)
        tree.show_root = not tree.show_root
