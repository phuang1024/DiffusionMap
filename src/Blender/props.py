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
    project_textures: bpy.props.StringProperty(
        name="Project textures",
        description="Path to local textures dir for this project.",
        default="//Textures",
    )

    source: bpy.props.EnumProperty(
        name="Source",
        description="Where the texture image comes from.",
        items=(
            ("0", "Local", "Local zip file or directory."),
            ("1", "Catalog", "Texture stored in the catalog."),
            ("2", "Web", "Search and download from AmbientCG."),
            ("3", "Diffusion", "Generate with a diffusion neural network."),
        ),
        default="0",
    )

    local_texture_path: bpy.props.StringProperty(
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
            #("4", "Add to catalog", "Add textures to catalog without importing."),
        ),
        default="2",
    )

    import_ref: bpy.props.EnumProperty(
        name="Reference",
        description="Which image files to reference from Image Texture(s).",
        items=(
            ("0", "Original", "Reference from original path. Can't be used with zip."),
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

    override_name: bpy.props.StringProperty(
        name="Override name",
        description="Override name of material and node group (blank to disable).",
    )
