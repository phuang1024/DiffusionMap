from torchvision.utils import make_grid, save_image

from AcgData import ColorDataset


def preview_data(args, dataset):
    samples = [dataset[i] for i in range(16)]
    grid = make_grid(samples, nrow=4)
    # TODO saving image and then having user open it is bad. Show in some GUI (e.g. opencv)
    save_image(grid, args.output)
