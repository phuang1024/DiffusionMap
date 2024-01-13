import argparse
from pathlib import Path

from .train import train


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path)
    parser.add_argument("results", type=Path)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--train_mult", type=int, default=5, help="Train for N epochs per epoch")
    parser.add_argument("--res", type=int, default=256)
    parser.add_argument("--unet_dim", type=int, default=64)
    parser.add_argument("--diffusion_steps", type=int, default=100)
    args = parser.parse_args()

    args.results.mkdir(exist_ok=True)

    train(args)


if __name__ == "__main__":
    main()
