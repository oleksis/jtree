from __future__ import annotations

from rich.highlighter import ReprHighlighter
from rich.json import JSON
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Tree, TreeNode

highlighter = ReprHighlighter()


class JSONDocument(Static):
    def load(self, json_data) -> bool:
        try:
            json_doc = JSON.from_data(json_data, indent=2)
        except Exception:
            return False
        self.update(json_doc)
        return True


class JSONTree(Tree):
    def add_node(self, name: str, node: TreeNode, data: object) -> None:
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
                self.add_node(key, new_node, value)
        elif isinstance(data, list):
            node._label = Text(f"[] {name}")
            for index, value in enumerate(data):
                new_node = node.add("")
                self.add_node(str(index), new_node, value)
        else:
            node._allow_expand = False
            if name:
                label = Text.assemble(
                    Text.from_markup(f"[b]{name}[/b]="), highlighter(repr(data))
                )
            else:
                label = Text(repr(data))
            node._label = label


class TreeView(Widget, can_focus_children=True):
    def compose(self) -> ComposeResult:
        tree = JSONTree("Root")
        tree.show_root = False
        yield tree
