from pathlib import Path

import bpy
from bpy.props import StringProperty

from .execute import execute_main, validate_settings, get_source


class DMAP_OT_Main(bpy.types.Operator):
    """Execute the flow from source to destination."""
    bl_idname = "dmap.main"
    bl_label = "Go"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        validate = validate_settings(context)
        if validate is not None:
            self.report({"ERROR"}, validate)
            return {"CANCELLED"}
        else:
            execute_main(self, context)
            return {"FINISHED"}


class DMAP_OT_ExportSource(bpy.types.Operator):
    # TODO when the fileselector appears, it selects a directory but looks like it selects a file. Maybe blender bug?
    """Export the source texture to a local file."""
    bl_idname = "dmap.export_source"
    bl_label = "Export to file"
    bl_options = {"REGISTER"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        source = get_source(context)
        export_path = source.export(Path(self.directory))
        self.report({"INFO"}, f"Exported to {export_path}")
        return {"FINISHED"}
