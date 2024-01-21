import bpy
from bpy.props import *

from .icons import load_importer_icon


class DMAP_Asset(bpy.types.PropertyGroup):
    """Asset data structure for the texture list."""
    id: StringProperty()
    # Space separated available resolutions, e.g. "1 2 4 8"
    res: StringProperty()
    # os.path.pathsep separated paths corresponding to resolutions.
    path: StringProperty()


class DMAP_Prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    catalog_path: StringProperty(
        name="Catalog path",
        description="Path to catalog (local textures storage bank) dir.",
        subtype="DIR_PATH",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "catalog_path")


def get_texlist_res_items(self, context):
    """Callback for texlist resolution selector Enum."""
    props = context.scene.dmap

    index = props.texlist_index
    if index >= len(props.texlist):
        return []

    items = []
    for res in props.texlist[index].res.split():
        items.append((res, f"{res}K", f"{res}K resolution."))

    return items


class DMAP_Props(bpy.types.PropertyGroup):
    project_textures: StringProperty(
        name="Project textures",
        description="Path to local textures dir for this project.",
        default="//Textures",
    )

    # Source

    source: EnumProperty(
        name="Source",
        description="Where the texture image comes from.",
        items=(
            ("0", "Local", "Local zip file or directory."),
            ("1", "Catalog", "Texture stored in the catalog."),
            ("2", "Web", "Search and download from AmbientCG."),
            ("3", "Diffusion", "Generate with a diffusion neural network."),
        ),
        default="0",
        update=load_importer_icon,
    )

    local_texture_path: StringProperty(
        name="Path",
        description="Path to material zip or dir.",
        subtype="FILE_PATH",
        default="",
        update=load_importer_icon,
    )

    web_query: StringProperty(
        name="Query",
        description="Search query for AmbientCG.",
        default="",
    )

    web_limit: IntProperty(
        name="Limit",
        description="Maximum number of results to display.",
        default=10,
        min=1,
        max=100,
    )

    texlist: CollectionProperty(type=DMAP_Asset)
    texlist_index: IntProperty(update=load_importer_icon)
    texlist_res: EnumProperty(items=get_texlist_res_items)

    # Import destination

    import_enabled: BoolProperty(
        name="Import material node group",
        description="Whether to import texture as PBR material node group.",
        default=True,
    )

    import_action: EnumProperty(
        name="Destination",
        items=(
            ("0", "Node group", "Create shader node group."),
            ("1", "Material", "Create material datablock."),
            ("2", "Current slot", "Create material and assign to current (selected) material slot."),
            ("3", "New slot", "Create material and assign to new material slot."),
        ),
        default="2",
    )

    import_ref: EnumProperty(
        name="Reference",
        description="Which image files to reference from Image Texture(s).",
        items=(
            ("0", "Original", "Reference from original path. Can't be used with zip."),
            ("1", "Project", "Copy to and use project textures path. Blend must be saved."),
            ("2", "Catalog", "Copy to and use catalog path."),
        ),
        default="0",
    )

    copy_type: EnumProperty(
        name="Copy type",
        description="Copy or symlink to project textures path.",
        items=(
            ("0", "Copy", "Copy files. Uses more disk space."),
            ("1", "Symlink", "Symlink files. Uses less disk space."),
        ),
        default="1",
    )

    override_name: StringProperty(
        name="Override name",
        description="Override name of material and node group (blank to disable).",
    )

    # Catalog destination

    catalog_enabled: BoolProperty(
        name="Add to catalog",
        description="Whether to add texture to catalog.",
        default=True,
    )
