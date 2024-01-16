from pathlib import Path

import bpy

from .importer import do_import_action


class DMAP_OT_ImportFile(bpy.types.Operator):
    """Import material from zip or dir."""
    bl_idname = "dmap.import_file"
    bl_label = "Import Material"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.dmap

        path = Path(props.i_path)
        name = path.stem.rsplit("_", 1)[0]

        do_import_action(name, props.i_path, props.i_import_action, self.report)

        return {"FINISHED"}
