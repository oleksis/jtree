# jtree
jtree is a command interface for displaying JSON (JavaScript Object Notation). It is based on the [Textual](textual.textualize.io/) a TUI (Text User Interface) framework for Python.

## Install
```bash
➜ python -m pip install jfree
```

## Usage
```bash
➜ kubectl --kubeconfig .\napptive-kubeconfig get deployment -ojson > deployment.json

➜ python -m jtree .\deployment.json
```

![jtree TUI](https://raw.githubusercontent.com/oleksis/jtree/main/json-tree.svg)
