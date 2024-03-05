"""
Data structure for handling texture storage.
See docs for file structure.
"""

import shutil
from enum import Enum
from pathlib import Path
from tempfile import mkdtemp
from zipfile import ZipFile

# Tmp used for unzipping.
ASSET_TMP = Path(mkdtemp())


def get_name_res(filename: str):
    """
    Ground012_1K
    Ground012_1K-JPG
    Ground012_1K-JPG.zip
    -> ("Ground012", 1)
    """
    name = filename.split("_")[0]
    res = int(filename.split("_")[1].split("-")[0][:-1])
    return name, res


class Asset:
    def __init__(self, path):
        self.path = Path(path)

        if self.path.stem.isdigit():
            self.res = int(self.path.stem)
            self.name = self.path.parent.name
        else:
            self.name, self.res = get_name_res(self.path.stem)
        self.id = f"{self.name}_{self.res}K"

        # Unzip into tmpdir if path is zip.
        if self.path.is_file():
            with ZipFile(self.path, "r") as zip:
                tmpdir = ASSET_TMP / self.id
                zip.extractall(tmpdir)
            self.path = Path(tmpdir)

    def get_maps(self) -> dict[str, Path]:
        """
        Returns dict of map name to absolute file path.
        """
        maps = {}
        for f in self.path.iterdir():
            name = f.name.lower()
            if "color" in name:
                maps["color"] = f
            elif "ambientocclusion" in name:
                maps["ao"] = f
            elif "displacement" in name:
                maps["disp"] = f
            elif "normalgl" in name:
                maps["nrm"] = f
            elif "roughness" in name:
                maps["rough"] = f
            if "_" not in name:
                maps["preview"] = f

        return maps

    def copy_to(self, path: Path):
        dest_path = path / self.id
        dest_path.mkdir(exist_ok=True, parents=True)
        for f in self.path.iterdir():
            shutil.copy(f, dest_path)

        return dest_path


class CatalogType(Enum):
    """See docs for description."""
    GLOBAL = 1
    PROJECT = 2


class Catalog:
    def __init__(self, type, root):
        self.type = type
        self.root = Path(root)

    def get_asset(self, name, res) -> Asset:
        if self.type == CatalogType.GLOBAL:
            path = self.root / name / str(res)
        elif self.type == CatalogType.PROJECT:
            path = self.root / f"{name}_{res}K"
        else:
            raise ValueError("Invalid catalog type.")

        return Asset(path)

    def get_asset_path(self, name, res) -> Path:
        return self.get_asset(name, res).path

    def copy_textures(self, source: Asset, symlink: bool = False):
        """
        Copy external textures to this catalog.
        Destination path is determined by the name and resolution of the source path.

        source: Source Asset object.
        symlink: if True, create symlink instead of copying.
        """
        target_path = self.get_asset_path(source.name, source.res)

        if target_path.exists():
            return

        target_path.parent.mkdir(exist_ok=True, parents=True)
        if symlink:
            target_path.symlink_to(source.path, target_is_directory=True)
        else:
            shutil.copytree(source.path, target_path, dirs_exist_ok=True)

        return target_path

    def iter_textures(self) -> dict[str, dict[int, str]]:
        """
        return {
            "Asset001": {
                1: /path/to/Asset001_1K,
                ...
            }
            ...
        }
        """
        textures = {}
        for asset in self.root.iterdir():
            if asset.is_dir():
                if self.type == CatalogType.GLOBAL:
                    name = asset.name
                    if name not in textures:
                        textures[name] = {}
                    for res in asset.iterdir():
                        if res.is_dir():
                            textures[name][int(res.name)] = res
                elif self.type == CatalogType.PROJECT:
                    name, res = get_name_res(asset.name)
                    if name not in textures:
                        textures[name] = {}
                    textures[name][res] = asset

        return textures
