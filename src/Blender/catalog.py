"""
Data structure for handling texture storage.
See docs for file structure.
"""

import shutil
from enum import Enum
from pathlib import Path
from zipfile import ZipFile

import bpy


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

    def get_maps(self) -> dict[str, Path]:
        """
        Returns dict of map name to absolute file path.
        """
        if self.path.is_file():
            raise ValueError("Cannot get maps of zip Asset.")

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

    def export(self, path: Path):
        export_path = path / self.id
        export_path.mkdir(exist_ok=True, parents=True)
        for f in self.path.iterdir():
            shutil.copy(f, export_path)

        return export_path


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

    def copy_textures(self, tx_path: Path):
        """
        Copy external textures to this catalog.
        Destination path is determined by the name and resolution of the source path.

        tx_path: e.g. /tmp/Ground012_1K-JPG or /tmp/Ground012_1K-JPG.zip
        """
        name, res = get_name_res(tx_path.name)
        target_path = self.get_asset_path(name, res)

        if tx_path.is_dir():
            target_path.parent.mkdir(exist_ok=True, parents=True)
            shutil.copytree(tx_path, target_path, dirs_exist_ok=True)
        elif tx_path.is_file():
            target_path.mkdir(exist_ok=True, parents=True)
            with ZipFile(tx_path, "r") as zip:
                zip.extractall(target_path)

        return target_path

    def iter_textures(self) -> dict[str, dict[str, int]]:
        """
        return {
            Asset001: {
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
