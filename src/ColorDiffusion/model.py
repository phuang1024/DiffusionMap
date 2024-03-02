import torch

from denoising_diffusion_pytorch import Unet, GaussianDiffusion

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_model(unet_dim, unet_dim_mults, timesteps, resolution):
    model = Unet(
        dim=unet_dim,
        dim_mults=unet_dim_mults,
        flash_attn=True,
    ).to(device)

    diffusion = GaussianDiffusion(
        model,
        timesteps=timesteps,
        image_size=resolution,
    ).to(device)

    return model, diffusion
