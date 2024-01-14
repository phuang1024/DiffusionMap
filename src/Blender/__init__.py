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


classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)