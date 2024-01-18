__all__ = (
    "load_icon",
    "get_icon",
)

"""
Handles loading icons for bpy.
"""

import bpy
import bpy.utils.previews

icons_global = None


def load_icon(path: str, key: str):
    assert icons_global is not None
    if key in icons_global:
        icons_global.remove(key)
    icons_global.load(key, path, 'IMAGE')


def get_icon(key: str):
    assert icons_global is not None
    return icons_global.get(key).icon_id


def register_icons():
    global icons_global
    if icons_global is None:
        icons_global = bpy.utils.previews.new()


def unregister_icons():
    global icons_global
    if icons_global:
        bpy.utils.previews.remove(icons_global)
        icons_global = None
