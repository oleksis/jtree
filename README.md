# jtree
jtree is a command line interface (CLI) for displaying JavaScript Object Notation (JSON) in a tree view powered by [Textual](https://textual.textualize.io/) a Text User Interface (TUI) framework for Python.

## Install
```bash
➜ python -m pip install jtree
```

## Usage
```pwsh
➜ kubectl --kubeconfig .\napptive-kubeconfig get deployment -ojson > deployment.json

➜ jtree tests/fixtures/deployment.json
```

![jtree TUI](https://raw.githubusercontent.com/oleksis/jtree/main/json-tree.svg)

Pass the JSON content to standard input (`sys.stdin`)
```bash
➜ pipdeptree --json-tree -p textual | jtree
```
