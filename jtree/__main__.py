from __future__ import annotations

import argparse
import json
import logging
import platform
import sys

from jtree import JSONTreeApp

WINDOWS = platform.system() == "Windows"
DEBUGPY_PORT = 5678


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
    parser.add_argument(
        "--log", nargs="?", help="Log level for enable debugpy", default="INFO"
    )

    args = parser.parse_args()
    json_data = None
    numeric_level = getattr(logging, args.log.upper(), None)

    if not isinstance(numeric_level, int):
        print(f"Invalid log level {args.log!r}")

    if numeric_level == logging.DEBUG:
        import debugpy

        debugpy.listen(DEBUGPY_PORT)
        debugpy.wait_for_client()

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
