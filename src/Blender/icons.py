"""
Handles loading icons for bpy.
"""

import os

import bpy
import bpy.utils.previews

icons_global = {}


def unregister_icons():
    for collection in icons_global.values():
        bpy.utils.previews.remove(collection)
    icons_global.clear()


def load_icon(key1: str, key2: str, path: str):
    if key1 not in icons_global:
        icons_global[key1] = bpy.utils.previews.new()
    icons_global[key1].load(key2, path, 'IMAGE', force_reload=True)

def get_icon(key1: str, key2: str):
    assert key1 in icons_global
    return icons_global[key1].get(key2).icon_id

def clear_icons(key1):
    if key1 in icons_global:
        bpy.utils.previews.remove(icons_global[key1])
        del icons_global[key1]

def icon_exists(key1: str, key2: str):
    return key1 in icons_global and key2 in icons_global[key1]


def get_preview_file(path):
    # TODO this should be integrated with Catalog
    if os.path.isdir(path):
        for file in os.listdir(path):
            if "_" not in file and file.endswith((".jpg", ".png")):
                return os.path.join(path, file)

    return None

def load_importer_icon(self, context):
    """update callback for property."""
    tx_path = bpy.path.abspath(context.scene.dmap.local_texture_path)
    preview_path = get_preview_file(tx_path)
    clear_icons("importer")
    if preview_path is not None:
        load_icon("importer", "preview", preview_path)
