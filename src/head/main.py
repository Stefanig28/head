from pathlib import Path
from typing import TextIO
import sys
import io


def main(
    files: list[TextIO | Path],
    output: io.StringIO = sys.stdout,
    lines: int | None = None,
    bytes: int | None = None,
) -> None:
    for i, file in enumerate(files):
        if isinstance(file, Path):
            file_name = file.name
        else:
            file_name = "stdin"

        if len(files) > 1:
            output.write(f"==> {file_name} <==\n")

        if bytes:
            if isinstance(file, Path):
                data = file.read_bytes()[:bytes].decode("utf-8", errors="ignore")
            else:
                data = file.read(bytes)

            output.write(data)
        else:
            if isinstance(file, Path):
                lines_out = file.read_text().splitlines()
            else:
                lines_out = file.read().splitlines()

            n = lines if lines else 10
            output.write("\n".join(lines_out[:n]) + "\n")

        if i < len(files) - 1:
            output.write("\n")


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_cchead = subparsers.add_parser("cchead")
    parser_cchead.add_argument("files", nargs="*", type=Path, default=[])
    parser_cchead.add_argument("-n", "--lines", type=int, default=None)
    parser_cchead.add_argument("-c", "--bytes", type=int, default=None)

    args = parser.parse_args()

    files = args.files

    if not files and not sys.stdin.isatty():
        files = [sys.stdin]

    main(files=files, lines=args.lines, bytes=args.bytes)


if __name__ == "__main__":
    _cli()
