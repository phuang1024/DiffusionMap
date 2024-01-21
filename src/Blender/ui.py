import bpy

from .icons import icon_exists, get_icon


class DMAP_UL_TextureList(bpy.types.UIList):
    """Draw a list of textures."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if icon_exists("texlist", item.id):
            icon = get_icon("texlist", item.id)
        layout.label(text=item.id, icon_value=icon)


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
        def draw_texlist(layout):
            col = layout.column(align=True)
            col.operator("dmap.texlist_refresh", icon="FILE_REFRESH")
            col.template_list("DMAP_UL_TextureList", "", props, "texlist", props, "texlist_index", rows=4)

            # TODO the text is not centered, because it's in a box. Blender bug?
            layout.prop(props, "texlist_res", expand=True)

        def draw_dropdown(layout, prop, text):
            icon = "TRIA_DOWN" if getattr(props, prop) else "TRIA_RIGHT"
            col = layout.column(align=True)
            col.prop(props, prop, text=text, toggle=True, icon=icon)
            box = col.box()
            return box

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

        elif props.source == "1":
            draw_texlist(box)

        elif props.source == "2":
            draw_texlist(box)

            subcol = box.column(align=True)
            row = subcol.row(align=True)
            row.prop(props, "web_query")
            row.prop(props, "web_limit")
            subcol.operator("dmap.web_search", icon="VIEWZOOM")

        if icon_exists("importer", "preview"):
            box.template_icon(get_icon("importer", "preview"), scale=5)

        box.separator()

        box.operator("dmap.export_source", icon="EXPORT")

        layout.separator(factor=3)

        # Import destination
        box = draw_dropdown(layout, "import_enabled", "Import material node group")

        if props.import_enabled:
            box.prop(props, "import_action")
            box.prop(props, "override_name")
            box.prop(props, "import_ref")
            if props.import_ref == "1":
                box.prop(props, "copy_type")

        layout.separator(factor=3)

        # Catalog destination
        box = draw_dropdown(layout, "catalog_enabled", "Add to catalog")

        if props.catalog_enabled:
            if props.source == "1":
                box.label(text="Source is catalog, nothing to do.", icon="INFO")
            else:
                box.label(text="Will add to catalog.")

        layout.separator(factor=3)

        # Go
        row = layout.row()
        row.scale_y = 2
        row.operator("dmap.main", icon="MATERIAL")
