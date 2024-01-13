__all__ = (
    "ColorDataset",
)

from pathlib import Path

import torchvision.transforms as T
from torch.utils.data import Dataset
from torchvision.io import read_image


class ColorDataset(Dataset):
    """
    Returns color maps from downloaded AmbientCG data.
    """

    def __init__(self, data_dir: Path, res: int, use_augment: bool = True, image_scale: float = 1.0):
        """
        data_dir: Path to the directory containing the downloaded AmbientCG data.
        res: Resolution of the returned images.
        use_augment: Whether to use data augmentation.
        image_scale: Scale (i.e. zooming in) of the returned images, as part of augmentation.
        """
        super().__init__()

        self.data_dir = data_dir
        self.res = res
        self.use_augment = use_augment

        self.assets = []
        for asset_dir in data_dir.iterdir():
            if asset_dir.is_dir():
                self.assets.append(asset_dir)

        self.resize = T.Resize((self.res, self.res), antialias=True)

        if use_augment:
            self.augment = T.Compose([
                T.RandomHorizontalFlip(),
                T.RandomVerticalFlip(),
                T.RandomResizedCrop(self.res, (0.5*image_scale, image_scale), ratio=(1, 1), antialias=True),
                T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.01),
            ])

    def __len__(self):
        return len(self.assets)

    def __getitem__(self, idx):
        asset_dir = self.assets[idx]
        image_path = asset_dir / "color.jpg"
        image = read_image(str(image_path))

        image = image.float() / 255.0
        image = self.resize(image)
        if self.use_augment:
            image = self.augment(image)

        return image
