__all__ = (
    "DMAP_OT_Main",
)

import bpy

from .catalog import Asset, Catalog, CatalogType
from .importer import import_material


class DMAP_OT_Main(bpy.types.Operator):
    """Execute the flow from source to destination."""
    bl_idname = "dmap.main"
    bl_label = "Go"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        validate = validate_settings(context)
        if validate is not None:
            self.report({"ERROR"}, validate)
            return {"CANCELLED"}
        else:
            execute_main(self, context)
            return {"FINISHED"}


def get_source(context) -> Asset:
    """
    Returns Asset defined by props.source et al.
    """
    props = context.scene.dmap

    if props.source == "0":
        path = bpy.path.abspath(props.local_texture_path)
        return Asset(path)

    elif props.source == "1":
        raise NotImplementedError()

    elif props.source == "2":
        raise NotImplementedError()

    elif props.source == "3":
        raise NotImplementedError()

    raise RuntimeError("This should never happen.")


def execute_import(self, context, source: Asset):
    props = context.scene.dmap
    prefs = context.preferences.addons[__package__].preferences

    if props.import_ref == "0":
        path = source.path

    elif props.import_ref in ("1", "2"):
        if props.import_ref == "1":
            archive_path = props.project_textures
            archive_type = CatalogType.PROJECT
        else:
            archive_path = prefs.catalog_path
            archive_type = CatalogType.GLOBAL
        archive = Catalog(archive_type, bpy.path.abspath(archive_path))

        path = archive.copy_textures(source.path)
        path = str(path)

    else:
        raise RuntimeError("This should never happen.")

    asset = Asset(path)
    maps = asset.get_maps()
    name = props.override_name if props.override_name else asset.name
    import_material(name, maps, props.import_action, self.report)


def execute_copy_to_catalog(self, context, source: Asset):
    props = context.scene.dmap
    prefs = context.preferences.addons[__package__].preferences

    if props.import_ref != "2":
        catalog = Catalog(CatalogType.GLOBAL, bpy.path.abspath(prefs.catalog_path))
        catalog.copy_textures(source.path)


def execute_main(self, context):
    """
    Call this from operator to load material.

    self, context: Passed from operator.
    """
    props = context.scene.dmap

    source = get_source(context)

    if props.import_enabled:
        execute_import(self, context, source)

    if props.catalog_enabled:
        execute_copy_to_catalog(self, context, source)


def validate_settings(context) -> str | None:
    """
    return: str = error message; None = validated.
    """
    return None  # TODO test

    props = context.scene.dmap
    prefs = context.preferences.addons[__package__].preferences
    local_texture_path = bpy.path.abspath(props.local_texture_path)

    if not os.path.exists(local_texture_path):
        return "Path does not exist."

    if props.import_ref == "0":
        if os.path.isfile(local_texture_path):
            return "Reference Original: Path must be directory (cannot be a zip file)."
    if props.import_ref == "1":
        if not bpy.data.is_saved:
            return "Reference Project: Blend must be saved."
    if props.import_ref == "2":
        if not prefs.catalog_path:
            return "Reference Catalog: Catalog path not set."

    if props.save_to_catalog and not prefs.catalog_path:
        return "Save to catalog: Catalog path not set."

    return None
