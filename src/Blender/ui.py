import bpy

from .icons import *


class BasePanel:
    """Base panel."""
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}


class DMAP_PT_Main(BasePanel, bpy.types.Panel):
    bl_label = "Diffusion Map"
    bl_idname = "DMAP_PT_Main"

    def draw(self, context):
        layout = self.layout
        props = context.scene.dmap

        layout.prop(props, "project_textures")

        layout.separator()

        # Source
        col = layout.column(align=True)

        col_source_prop = col.column(align=True)
        row1 = col_source_prop.row(align=True)
        row1.prop_enum(props, "source", "0")
        row1.prop_enum(props, "source", "1")
        row2 = col_source_prop.row(align=True)
        row2.prop_enum(props, "source", "2")
        row2.prop_enum(props, "source", "3")

        box = col.box()

        if props.source == "0":
            box.prop(props, "local_texture_path")

            if icon_exists("importer", "preview"):
                box.template_icon(get_icon("importer", "preview"), scale=5)

        layout.prop(props, "import_action")
        layout.prop(props, "override_name")

        layout.operator("dmap.import_from_file", icon="MATERIAL")


"""
class DMAP_PT_Importer(BasePanel, bpy.types.Panel):
    bl_label = "Importer"
    bl_parent_id = "DMAP_PT_Main"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.scene.dmap

        layout.prop(props, "import_path")

        if props.import_action != "4":
            layout.prop(props, "import_ref")

            col = layout.column()
            col.prop(props, "save_to_catalog")
            col.enabled = (props.import_ref != "2")

        layout.operator("dmap.import_from_file", icon="MATERIAL")

        if icon_exists("importer", "preview"):
            layout.template_icon(get_icon("importer", "preview"), scale=10)
"""
