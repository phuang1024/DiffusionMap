bl_info = {
    "name": "Diffusion Map",
    "description": "AI tools for Blender materials.",
    "author": "Patrick Huang",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Properties > Material > Diffusion Map",
    "doc_url": "https://github.com/phuang1024/DiffusionMap",
    "tracker_url": "https://github.com/phuang1024/DiffusionMap/issues",
    "category": "Material",
}

import bpy

from .ops import *
from .props import *
from .ui import *


classes = (
    DMAP_Props,

    DMAP_OT_ImportFile,

    DMAP_PT_Main,
    DMAP_PT_Importer,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dmap = bpy.props.PointerProperty(type=DMAP_Props)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.dmap
