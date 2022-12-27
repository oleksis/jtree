from __future__ import annotations

import json
import sys
import tempfile
from typing import TYPE_CHECKING

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer, Header

from jtree.widgets import JSONDocument, JSONTree, TreeView

if TYPE_CHECKING:
    from io import TextIOWrapper

__prog_name__ = "jtree"
__version__ = "0.2.2"


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
        with tempfile.TemporaryFile() as fp_temp:
            if json_file is sys.stdin:
                fp_temp.write(sys.stdin.read().encode(encoding="utf-8"))
            else:
                fp_temp.write(json_file.read().encode(encoding="utf-8"))
                json_file.close()
            fp_temp.seek(0)
            self.json_data = fp_temp.read().decode("utf-8")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            TreeView(id="tree-view"), JSONDocument(id="json-document"), id="app-grid"
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
