from denoising_diffusion_pytorch import Unet, GaussianDiffusion


def create_model(args):
    model = Unet(
        dim=args.unet_dim,
        dim_mults=(1, 2, 4, 8),
        flash_attn=True,
    )

    diffusion = GaussianDiffusion(
        model,
        timesteps=args.diffusion_steps,
        image_size=args.res,
    )

    return model, diffusion
