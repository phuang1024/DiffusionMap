import argparse
from pathlib import Path

from .download_data import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("-q", type=str, default="")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--bs", type=int, default=20)
    parser.add_argument("--sbsar", action="store_true", help="Download sbsar instead of textures.")
    args = parser.parse_args()

    download_data(args)


if __name__ == "__main__":
    main()
