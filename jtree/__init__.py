from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer, Header

from jtree.widgets import JSONDocument, JSONTree, TreeView

__version__ = "0.2.0"


class JSONTreeApp(App):
    TITLE = "jtree"
    CSS_PATH = "css/layout.css"

    BINDINGS = [
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("ctrl+t", "toggle_root", "Toggle root"),
        Binding("ctrl+q", "app.quit", "Quit"),
    ]

    def __init__(
        self, json_data=None, driver_class=None, css_path=None, watch_css=False
    ):
        self.json_data = json_data
        super().__init__(driver_class, css_path, watch_css)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            TreeView(id="tree-view"), JSONDocument(id="json-document"), id="app-grid"
        )

    def on_mount(self) -> None:
        tree = self.query_one(JSONTree)
        root_name = "JSON"
        json_node = tree.root.add(root_name)
        tree.add_node(root_name, json_node, self.json_data)
        json_doc = self.query_one(JSONDocument)
        json_doc.load(self.json_data)

    def action_screenshot(self):
        self.save_screenshot("./json-tree.svg")

    def action_toggle_root(self) -> None:
        tree = self.query_one(JSONTree)
        tree.show_root = not tree.show_root
