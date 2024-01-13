import argparse
from pathlib import Path

from .preview_data import preview_data
from .train import train


def main():
    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers(dest="action")

    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)

    parser.add_argument("--res", type=int, default=256)

    train_p = subp.add_parser("train")
    train_p.add_argument("--epochs", type=int, default=100)
    train_p.add_argument("--train_mult", type=int, default=5, help="Repeat train dataset N times per epoch")
    train_p.add_argument("--test_interval", type=int, default=5)
    train_p.add_argument("--batch_size", type=int, default=4)
    train_p.add_argument("--unet_dim", type=int, default=64)
    train_p.add_argument("--diffusion_steps", type=int, default=100)

    data_p = subp.add_parser("view_data")

    args = parser.parse_args()

    if args.action == "train":
        args.output.mkdir(exist_ok=True)
        train(args)

    elif args.action == "view_data":
        preview_data(args)


if __name__ == "__main__":
    main()
