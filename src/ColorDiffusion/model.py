import torch

from denoising_diffusion_pytorch import Unet, GaussianDiffusion

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_model(args):
    model = Unet(
        dim=args.unet_dim,
        dim_mults=(1, 2, 4, 8),
        flash_attn=True,
    ).to(device)

    diffusion = GaussianDiffusion(
        model,
        timesteps=args.diffusion_steps,
        image_size=args.res,
    ).to(device)

    return model, diffusion
