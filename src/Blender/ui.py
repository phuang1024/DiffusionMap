import bpy

from .icons import *


class BasePanel:
    """Base panel."""
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}


class DMAP_PT_Main(BasePanel, bpy.types.Panel):
    """Main panel."""
    bl_label = "Diffusion Map"
    bl_idname = "DMAP_PT_Main"

    def draw(self, context):
        layout = self.layout
        props = context.scene.dmap

        layout.prop(props, "project_textures")

        layout.separator()

        layout.prop(props, "import_action")
        layout.prop(props, "override_name")


class DMAP_PT_Importer(BasePanel, bpy.types.Panel):
    """Importer panel."""
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
