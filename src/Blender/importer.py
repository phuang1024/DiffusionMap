"""
Functions for material importer.
"""

import os

import bpy

from .icons import *
from .material import import_material


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


def importer_main(name, path, action, report):
    """
    Call this from operator to load material.

    name: Name of material and node group.
    path: Path to zip file or textures directory.
    action: props.import_action
    report: self.report (function).
    """
    if path.endswith(".zip"):
        with TemporaryDirectory() as tmp, ZipFile(path) as zip:
            zip.extractall(tmp)
            maps = get_map_files(tmp)
            import_material(name, maps, action, report)

    else:
        maps = get_map_files(path)
        import_material(name, maps, action, report)


def validate_settings(context) -> str | None:
    """
    return: str = error message; None = validated.
    """
    props = context.scene.dmap
    prefs = context.preferences.addons[__package__].preferences

    if not os.path.exists(props.import_path):
        return "Path does not exist."

    if props.import_ref == "0":
        if os.path.isfile(props.import_path):
            return "Reference File: Path must be directory (cannot be a zip file)."
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
    tx_path = context.scene.dmap.import_path
    preview_path = get_preview_file(tx_path)
    clear_icons("importer")
    if preview_path is not None:
        load_icon("importer", "preview", preview_path)
