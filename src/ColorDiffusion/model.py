import torch

from denoising_diffusion_pytorch import Unet, GaussianDiffusion

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_model(image_res):
    model = Unet(
        dim=32,
        dim_mults=(1, 2, 4, 8),
        flash_attn=True,
    ).to(device)

    diffusion = GaussianDiffusion(
        model,
        timesteps=1000,
        image_size=image_res,
    ).to(device)

    return model, diffusion
