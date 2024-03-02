from tqdm import tqdm

import torch
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter
from torchvision.utils import make_grid, save_image

from AcgData import ColorDataset
from .model import create_model, device


def train(config):
    config["results"].mkdir(exist_ok=True)
    dataset = ColorDataset(config["data"], config["resolution"], image_scale=1)

    train_size = int(len(dataset) * 0.9)
    train_dset, test_dset = random_split(dataset, [train_size, len(dataset) - train_size])
    loader_args = dict(batch_size=config["batch_size"], shuffle=True, num_workers=8)
    train_loader = DataLoader(train_dset, **loader_args)
    test_loader = DataLoader(test_dset, **loader_args)

    model, diffusion = create_model(
        config["unet_dim"],
        config["unet_dim_mults"],
        config["timesteps"],
        config["resolution"],
    )

    if config["resume"]:
        print("Resuming from", config["resume"])
        model.load_state_dict(torch.load(config["resume"]))

    lr_decay = (config["lr_end"] / config["lr_start"]) ** (1 / config["epochs"])
    optim = torch.optim.Adam(model.parameters(), lr=config["lr_start"])
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optim, gamma=lr_decay)

    writer = SummaryWriter(config["results"] / "logs")

    step = 0
    for epoch in range(1, config["epochs"]+1):
        pbar = tqdm(range(config["train_duplicity"] * len(train_loader)))
        for _ in range(config["train_duplicity"]):
            for x in train_loader:
                x = x.to(device)
                loss = diffusion(x)
                loss /= config["grad_accum"]
                loss.backward()

                if (step + 1) % config["grad_accum"] == 0:
                    optim.step()
                    optim.zero_grad()

                writer.add_scalar("train_loss", loss.item(), step)
                writer.add_scalar("lr", scheduler.get_last_lr()[0], step)

                desc = f"Train: Epoch {epoch};  Step {step};  Loss {loss.item():.4f};  LR {scheduler.get_last_lr()[0]:.1e}"
                pbar.set_description(desc)
                pbar.update(1)
                step += 1

        pbar.close()

        with torch.no_grad():
            pbar = tqdm(test_loader)
            avg_loss = 0
            for x in pbar:
                x = x.to(device)
                loss = diffusion(x)
                avg_loss += loss.item()
                pbar.set_description(f"Test: Epoch {epoch};  Loss {loss.item():.4f}")
            writer.add_scalar("test_loss", avg_loss / len(test_loader), step)

        if epoch % config["test_interval"] == 0:
            print(f"Generating fakes on epoch {epoch}")
            with torch.no_grad():
                generated = diffusion.sample(batch_size=9)
                grid = make_grid(generated, nrow=3)
                save_image(grid, config["results"] / f"epoch{epoch}.jpg")
                torch.save(model.state_dict(), config["results"] / f"epoch{epoch}.pt")

                writer.add_image("generated", grid, epoch)

        scheduler.step()
