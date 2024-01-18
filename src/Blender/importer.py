"""
Functions for material importer.
"""

import os
import shutil
from pathlib import Path
from zipfile import ZipFile

import bpy

from .icons import *
from .material import import_material
from .utils import get_name_res


def get_map_files(directory):
    """
    Returns dict of map name to absolute file path.
    """
    maps = {}

    for f in os.listdir(directory):
        name = os.path.basename(f).lower()
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

    maps = {k: os.path.join(directory, f) for k, f in maps.items()}
    return maps


def importer_main(self, context):
    """
    Call this from operator to load material.

    self, context: Passed from operator.

    name: Name of material and node group.
    path: Path to zip file or textures directory.
    action: props.import_action
    report: self.report (function).
    """
    props = context.scene.dmap

    original_path = Path(bpy.path.abspath(props.import_path))
    # TODO add override name feature.
    original_name, res = get_name_res(original_path.stem)

    if props.import_ref == "0":
        path = original_path

    elif props.import_ref in ("1", "2"):
        if props.import_ref == "1":
            project_textures = Path(bpy.path.abspath(props.project_textures))
            project_textures.mkdir(exist_ok=True, parents=True)
            path = project_textures / original_name / str(res)
        else:
            raise NotImplementedError

        if original_path.is_dir():
            path.parent.mkdir(exist_ok=True, parents=True)
            shutil.copytree(original_path, path, dirs_exist_ok=True)
        elif original_path.is_file():
            path.mkdir(exist_ok=True, parents=True)
            with ZipFile(original_path, "r") as zip:
                zip.extractall(path)

        path = str(path)

    else:
        raise RuntimeError("This should never happen.")

    maps = get_map_files(path)
    import_material(original_name, maps, props.import_action, self.report)


def validate_settings(context) -> str | None:
    """
    return: str = error message; None = validated.
    """
    props = context.scene.dmap
    prefs = context.preferences.addons[__package__].preferences
    import_path = bpy.path.abspath(props.import_path)

    if not os.path.exists(import_path):
        return "Path does not exist."

    if props.import_ref == "0":
        if os.path.isfile(import_path):
            return "Reference Original: Path must be directory (cannot be a zip file)."
    if props.import_ref == "1":
        if not bpy.data.is_saved:
            return "Reference Project: Blend must be saved."
    if props.import_ref == "2":
        if not prefs.catalog_path:
            return "Reference Catalog: Catalog path not set."

    return None


def get_preview_file(path):
    if os.path.isdir(path):
        for file in os.listdir(path):
            if "_" not in file and file.endswith((".jpg", ".png")):
                return os.path.join(path, file)

    return None

def load_importer_icon(self, context):
    tx_path = bpy.path.abspath(context.scene.dmap.import_path)
    preview_path = get_preview_file(tx_path)
    clear_icons("importer")
    if preview_path is not None:
        load_icon("importer", "preview", preview_path)
