from tqdm import tqdm

import torch
from torch.utils.data import DataLoader
from torchvision.utils import make_grid, save_image

from AcgData import ColorDataset
from .model import create_model, device


def train(args):
    dataset = ColorDataset(args.data, args.res)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)

    model, diffusion = create_model(args)
    optim = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(args.epochs):
        print(f"Train epoch {epoch}")
        pbar = tqdm(range(args.train_mult * len(loader)))
        step = 0
        for i in range(args.train_mult):
            for x in loader:
                x = x.to(device)
                loss = diffusion(x)
                loss.backward()
                optim.step()
                optim.zero_grad()

                desc = f"  Epoch {epoch};  Sample {step};  Loss {loss.item():.4f}"
                pbar.set_description(desc)
                pbar.update(1)
                step += 1

        print(f"Test epoch {epoch}")
        with torch.no_grad():
            generated = diffusion.sample(batch_size=16)
            grid = make_grid(generated, nrow=4)
            save_image(grid, args.results / f"epoch{epoch}.png")
            torch.save(model.state_dict(), args.results / f"epoch{epoch}.pt")
