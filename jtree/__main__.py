from __future__ import annotations

import argparse
import json
import platform
import sys

from jtree import JSONTreeApp

WINDOWS = platform.system() == "Windows"


def main():
    parser = argparse.ArgumentParser(description="Json Tree")
    parser.add_argument(
        "path",
        nargs="?",
        type=argparse.FileType(encoding="utf-8"),
        metavar="PATH",
        help="path to file, or stdin",
        default=sys.stdin,
    )

    args = parser.parse_args()
    json_data = None

    with args.path as infile:
        try:
            json_data = json.load(infile)

            # See:Textualize/textual/issues/153#issuecomment-1256933121
            if not WINDOWS:
                sys.stdin = open("/dev/tty", "r")

            app = JSONTreeApp(json_data)
            app.run()

            if not sys.stdin.closed:
                sys.stdin.close()

        except Exception as error:
            print(f"Unable to read {args.path!r}; {error}")
            sys.exit(-1)


if __name__ == "__main__":
    main()
