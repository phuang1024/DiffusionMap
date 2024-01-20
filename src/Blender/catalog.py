"""
Data structure for handling texture storage.
See docs for file structure.
"""

from enum import Enum
from pathlib import Path


class CatalogType(Enum):
    """See docs for description."""
    GLOBAL = 1
    PROJECT = 2


class Catalog:
    def __init__(self, type, root):
        self.type = type
        self.root = Path(root)

    def get_asset_path(self, name, res):
        if self.type == CatalogType.GLOBAL:
            return self.root / name / res
        elif self.type == CatalogType.PROJECT:
            return self.root / f"{name}_{res}K"
        raise ValueError("Invalid catalog type.")

    def get_map_files(self, name, res):
        """
        Returns dict of map name to absolute file path.
        """
        path = self.get_asset_path(name, res)
        maps = {}

        for f in path.iterdir():
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
