from __future__ import annotations

import argparse
import json
import sys

from rich.highlighter import ReprHighlighter
from rich.text import Text

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Tree, TreeNode


__version__ = "0.1.0"
highlighter = ReprHighlighter()


def add_node(name: str, node: TreeNode, data: object) -> None:
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
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("t", "toggle_root", "Toggle root"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Tree("Root")

    def on_mount(self) -> None:
        parser = argparse.ArgumentParser(description="Json Tree")
        parser.add_argument(
            "path",
            metavar="PATH",
            help="path to file, or - for stdin",
        )

        args = parser.parse_args()

        try:
            if args.path == "-":
                content = sys.stdin.read()
                # sys.stdin = open('/dev/tty', 'r')
                self.json_data = content
            else:
                with open(args.path, "rt") as json_file:
                    self.json_data = json.load(json_file)
        except Exception as error:
            self.log(f"Unable to read {args.path!r}; {error}")
            sys.exit(-1)

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
