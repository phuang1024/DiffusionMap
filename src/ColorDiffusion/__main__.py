import argparse
import json
from pathlib import Path

from AcgData import ColorDataset
from .preview_data import preview_data
from .train import train


def main():
    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers(dest="action")

    train_p = subp.add_parser("train")
    train_p.add_argument("--config", type=Path, required=True, help="Path to config json. See docs.")

    data_p = subp.add_parser("view_data")
    data_p.add_argument("--data", type=Path, required=True)

    args = parser.parse_args()

    if args.action == "train":
        with args.config.open() as f:
            config = json.load(f)
        config["data"] = Path(config["data"])
        config["results"] = Path(config["results"])

        train(config)

    elif args.action == "view_data":
        dataset = ColorDataset(args.data, 1024, image_scale=1)
        preview_data(args, dataset)


if __name__ == "__main__":
    main()
