import bpy


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
        pass


class DMAP_PT_Importer(BasePanel, bpy.types.Panel):
    """Importer panel."""
    bl_label = "Importer"
    bl_parent_id = "DMAP_PT_Main"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.scene.dmap

        layout.prop(props, "import_path")
        layout.prop(props, "import_action")

        layout.prop(props, "import_ref")
        layout.prop(props, "project_tx_path")
        layout.prop(props, "save_to_catalog")

        layout.operator("dmap.import_from_file", icon="MATERIAL")
