# jtree
jtree is a command interface for displaying JSON (JavaScript Object Notation). It is based on the [Textual](https://textual.textualize.io/) a TUI (Text User Interface) framework for Python.

## Install
```bash
➜ python -m pip install jtree
```

## Usage
```pwsh
➜ kubectl --kubeconfig .\napptive-kubeconfig get deployment -ojson > deployment.json

➜ python -m jtree .\deployment.json
```

![jtree TUI](https://raw.githubusercontent.com/oleksis/jtree/main/json-tree.svg)

Pass the JSON content to standard input (`sys.stdin`)
```bash
➜ pipdeptree --json-tree -p textual | python -m jtree
```
