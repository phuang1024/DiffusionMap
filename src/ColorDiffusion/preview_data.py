import matplotlib.pyplot as plt

from torchvision.utils import make_grid


def preview_data(args, dataset):
    samples = [dataset[i] for i in range(16)]
    grid = make_grid(samples, nrow=4)

    plt.imshow(grid.permute(1, 2, 0))
    plt.show()
