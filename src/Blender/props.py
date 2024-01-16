import bpy


class DMAP_Props(bpy.types.PropertyGroup):
    # Importer props

    i_path: bpy.props.StringProperty(
        name="Path",
        description="Path to material zip or dir.",
        subtype="FILE_PATH",
        default="",
    )

    i_import_action: bpy.props.EnumProperty(
        name="Action",
        items=(
            ("0", "Node group", "Create shader node group."),
            ("1", "Material", "Create material datablock."),
            ("2", "Current slot", "Create material and assign to current (selected) material slot."),
            ("3", "New slot", "Create material and assign to new material slot."),
        ),
        default="3",
    )
