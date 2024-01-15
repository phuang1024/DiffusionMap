import argparse
from pathlib import Path

from AcgData import ColorDataset
from .preview_data import preview_data
from .train import train


def main():
    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers(dest="action")

    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)

    parser.add_argument("--res", type=int, default=256)
    parser.add_argument("--image_scale", type=float, default=0.5, help="Passed to ColorDataset")

    train_p = subp.add_parser("train")
    train_p.add_argument("--resume", type=str)
    train_p.add_argument("--epochs", type=int, default=1001)
    train_p.add_argument("--lr", type=float, default=1e-4)
    train_p.add_argument("--train_mult", type=int, default=8, help="Repeat train dataset N times per epoch")
    train_p.add_argument("--test_interval", type=int, default=40)
    train_p.add_argument("--batch_size", type=int, default=8)
    train_p.add_argument("--grad_accum", type=int, default=4)

    data_p = subp.add_parser("view_data")

    args = parser.parse_args()

    dataset = ColorDataset(args.data, args.res, image_scale=args.image_scale)

    if args.action == "train":
        args.output.mkdir(exist_ok=True)
        train(args, dataset)

    elif args.action == "view_data":
        preview_data(args, dataset)


if __name__ == "__main__":
    main()
