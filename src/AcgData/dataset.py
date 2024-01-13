__all__ = (
    "ColorDataset",
)

from pathlib import Path

from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision.transforms import Resize


# TODO augmentations


class ColorDataset(Dataset):
    """
    Returns color maps from downloaded AmbientCG data.
    """

    def __init__(self, data_dir: Path, res: int):
        super().__init__()

        self.data_dir = data_dir
        self.res = res
        self.assets = []
        for asset_dir in data_dir.iterdir():
            if asset_dir.is_dir():
                self.assets.append(asset_dir)

        self.resize = Resize((self.res, self.res), antialias=True)

    def __len__(self):
        return len(self.assets)

    def __getitem__(self, idx):
        asset_dir = self.assets[idx]
        image_path = asset_dir / "color.jpg"
        image = read_image(str(image_path))
        image = image.float() / 255.0
        image = self.resize(image)
        return image
