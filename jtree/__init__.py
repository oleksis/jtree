from __future__ import annotations

from rich.highlighter import ReprHighlighter
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Tree, TreeNode

__version__ = "0.1.3"
highlighter = ReprHighlighter()


def add_node(name: str, node: TreeNode, data: object) -> None:
    """Adds a node to the tree.

    Args:
        name (str): Name of the node.
        node (TreeNode): Parent node.
        data (object): Data associated with the node.
    """
    if isinstance(data, dict):
        node._label = Text(f"{{}} {name}")
        for key, value in data.items():
            new_node = node.add("")
            add_node(key, new_node, value)
    elif isinstance(data, list):
        node._label = Text(f"[] {name}")
        for index, value in enumerate(data):
            new_node = node.add("")
            add_node(str(index), new_node, value)
    else:
        node._allow_expand = False
        if name:
            label = Text.assemble(
                Text.from_markup(f"[b]{name}[/b]="), highlighter(repr(data))
            )
        else:
            label = Text(repr(data))
        node._label = label


class JSONTreeApp(App):
    TITLE = "jtree"

    BINDINGS = [
        ("s", "app.screenshot()", "Screenshot"),
        ("t", "toggle_root", "Toggle root"),
        Binding("c, q", "app.quit", "Quit", show=True),
    ]

    def __init__(
        self, json_data=None, driver_class=None, css_path=None, watch_css=False
    ):
        self.json_data = json_data
        super().__init__(driver_class, css_path, watch_css)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Tree("Root")

    def on_mount(self) -> None:
        tree = self.query_one(Tree)
        root_name = "JSON"
        json_node = tree.root.add(root_name)
        add_node(root_name, json_node, self.json_data)
        tree.show_root = False

    def action_screenshot(self):
        self.save_screenshot("./json-tree.svg")

    def action_toggle_root(self) -> None:
        tree = self.query_one(Tree)
        tree.show_root = not tree.show_root
