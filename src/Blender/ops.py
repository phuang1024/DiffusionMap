import bpy

from .importer import importer_main, validate_settings


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
            importer_main(self, context)
            return {"FINISHED"}
