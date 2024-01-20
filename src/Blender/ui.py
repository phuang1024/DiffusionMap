import bpy

from .icons import icon_exists, get_icon


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

        layout.separator()

        # Import destination
        col = layout.column(align=True)
        col.prop(props, "import_enabled", toggle=True, text="Import material node group")
        box = col.box()

        if props.import_enabled:
            box.prop(props, "import_action")
            box.prop(props, "override_name")
            box.prop(props, "import_ref")

        layout.separator()

        # Catalog destination
        col = layout.column(align=True)
        col.prop(props, "catalog_enabled", toggle=True, text="Add to catalog")
        box = col.box()

        if props.catalog_enabled:
            if props.source == "1":
                box.label(text="Source is catalog, nothing to do.", icon="INFO")
            else:
                box.label(text="Will add to catalog.")

        layout.separator()

        # Go
        layout.operator("dmap.main", icon="MATERIAL")
