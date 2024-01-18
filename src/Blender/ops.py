import bpy

from .importer import importer_main, validate_settings


class DMAP_OT_ImportFile(bpy.types.Operator):
    """Import material from zip or dir."""
    bl_idname = "dmap.import_from_file"
    bl_label = "Import Material"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        validate = validate_settings(context)
        if validate is not None:
            self.report({"ERROR"}, validate)
            return {"CANCELLED"}
        else:
            importer_main(self, context)
            return {"FINISHED"}
