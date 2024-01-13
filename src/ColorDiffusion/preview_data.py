from torchvision.utils import make_grid, save_image

from AcgData import ColorDataset


def preview_data(args):
    dataset = ColorDataset(args.data, args.res)

    samples = [dataset[i] for i in range(16)]
    grid = make_grid(samples, nrow=4)
    save_image(grid, args.output)
