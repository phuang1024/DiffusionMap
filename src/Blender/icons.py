"""
Handles loading icons for bpy.
"""

import bpy
import bpy.utils.previews

from .execute import get_source

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


def load_importer_icon(self, context):
    """update callback for property."""
    clear_icons("source")

    try:
        source = get_source(context)
    except:
        return

    maps = source.get_maps()
    if "preview" in maps:
        load_icon("source", "preview", str(maps["preview"]))
