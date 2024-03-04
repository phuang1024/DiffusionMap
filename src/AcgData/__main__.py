import argparse
from pathlib import Path

from .download_data import *


def main():
    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers(dest="action")

    download = subp.add_parser("download")
    download.add_argument("output", type=Path)
    download.add_argument("-q", type=str, default="")
    download.add_argument("--count", type=int, default=100)
    download.add_argument("--bs", type=int, default=20)
    download.add_argument("--sbsar", action="store_true", help="Download sbsar instead of textures.")

    sbsar = subp.add_parser("render_sbsar")
    sbsar.add_argument("input", type=Path, help="Directory containing sbsars.")
    sbsar.add_argument("output", type=Path, help="Output directory.")
    sbsar.add_argument("--count", type=int, default=100)

    args = parser.parse_args()

    if args.action == "download":
        download_data(args)
    elif args.action == "render_sbsar":
        render_sbsar(args)


if __name__ == "__main__":
    main()
