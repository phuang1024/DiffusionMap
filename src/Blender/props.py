import bpy

from .importer import load_importer_icon


class DMAP_Prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    catalog_path: bpy.props.StringProperty(
        name="Catalog path",
        description="Path to catalog (local textures storage bank) dir.",
        subtype="DIR_PATH",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "catalog_path")


class DMAP_Props(bpy.types.PropertyGroup):
    # Importer props

    import_path: bpy.props.StringProperty(
        name="Path",
        description="Path to material zip or dir.",
        subtype="FILE_PATH",
        default="",
        update=load_importer_icon,
    )

    import_action: bpy.props.EnumProperty(
        name="Action",
        items=(
            ("0", "Node group", "Create shader node group."),
            ("1", "Material", "Create material datablock."),
            ("2", "Current slot", "Create material and assign to current (selected) material slot."),
            ("3", "New slot", "Create material and assign to new material slot."),
        ),
        default="3",
    )

    project_tx_path: bpy.props.StringProperty(
        name="Project textures",
        description="Path to local textures dir for this project.",
        default="//Textures",
    )

    import_ref: bpy.props.EnumProperty(
        name="Reference",
        description="Which image files to reference from Image Texture(s).",
        items=(
            ("0", "Given", "Reference from given path. Can't be used with zip."),
            ("1", "Project", "Copy to and use project textures path. Blend must be saved."),
            ("2", "Catalog", "Copy to and use catalog path."),
        ),
        default="0",
    )

    save_to_catalog: bpy.props.BoolProperty(
        name="Save to catalog",
        description="Also save textures to catalog.",
        default=True,
    )
