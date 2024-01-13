import argparse
from pathlib import Path

from .download_data import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=str)
    parser.add_argument("-q", type=str, default="")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--bs", type=int, default=20)
    args = parser.parse_args()

    download_data(Path(args.output), args.q, args.count, bs=args.bs)


if __name__ == "__main__":
    main()
