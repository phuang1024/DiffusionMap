"""
Code to run the main Execute operator.
"""

from pathlib import Path
from tempfile import mkdtemp

import bpy
import requests

from .catalog import Asset, Catalog, CatalogType
from .importer import import_material

TMPDIR = Path(mkdtemp())


def get_source(context, execute=False) -> Asset:
    """
    Returns Asset defined by props.source et al.

    execute: Whether this is called as part of the operator execute
        (as opposed to getting icon).
    """
    def get_texlist_choice():
        """
        Returns path (i.e. entry of DMAP_Asset.path) corresponding to selected resolution.
        """
        tex = props.texlist[props.texlist_index]
        for i, res in enumerate(tex.res.split()):
            if res == props.texlist_res:
                break
        else:
            raise RuntimeError("This should never happen.")
        path = tex.path.split(";")[i]
        return path

    props = context.scene.dmap

    if props.source == "0":
        path = bpy.path.abspath(props.local_texture_path)
        return Asset(path)

    elif props.source == "1":
        path = get_texlist_choice()
        return Asset(path)

    elif props.source == "2":
        if execute:
            url = get_texlist_choice()
            r = requests.get(url)
            r.raise_for_status()

            fname = f"{props.texlist[props.texlist_index].id}_{props.texlist_res}K-JPG.zip"
            path = TMPDIR / fname
            with open(path, "wb") as f:
                f.write(r.content)

            return Asset(path)
        else:
            raise NotImplementedError()

    elif props.source == "3":
        raise NotImplementedError()

    raise RuntimeError("This should never happen.")


def execute_import(self, context, source: Asset):
    props = context.scene.dmap
    prefs = context.preferences.addons[__package__].preferences

    # If source is web or diffusion AND reference Project with symlink,
    # textures need to be copied to catalog.
    if props.source in ("2", "3") and props.import_ref == "1" and props.copy_type == "1":
        execute_copy_to_catalog(self, context, source)
        catalog = Catalog(CatalogType.GLOBAL, bpy.path.abspath(prefs.catalog_path))
        source = catalog.get_asset(source.name, source.res)
        self.report({"INFO"}, "Reference Project with Symlink: Textures copied to Catalog.")

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

        path = archive.copy_textures(source, symlink=(props.copy_type == "1"))
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
        catalog.copy_textures(source)


def execute_main(self, context):
    """
    Call this from operator to load material.

    self, context: Passed from operator.
    """
    props = context.scene.dmap

    source = get_source(context, execute=True)

    if props.import_enabled:
        execute_import(self, context, source)

    if props.catalog_enabled:
        execute_copy_to_catalog(self, context, source)


def validate_settings(context) -> str | None:
    """
    return: str = error message; None = validated.
    """
    props = context.scene.dmap
    prefs = context.preferences.addons[__package__].preferences

    # Check import destination
    if props.import_enabled:
        if props.import_ref == "1":
            if not bpy.data.is_saved:
                return "Importer: Reference Project: Blend must be saved."
        if props.import_ref == "2":
            if not prefs.catalog_path:
                return "Importer: Reference Catalog: Catalog path not set."

    # Check catalog destination
    if props.catalog_enabled:
        if not prefs.catalog_path:
            return "Save to catalog: Catalog path not set."

    if props.source in ("0", "1"):
        # Check source
        if props.source == "0":
            local_texture_path = Path(bpy.path.abspath(props.local_texture_path))
            if not local_texture_path.exists() or not props.local_texture_path:
                return "Source: Local file: Path does not exist."

        # Check import destination
        source = get_source(context)
        if props.import_enabled:
            if props.import_ref == "0":
                if not source.path.is_dir():
                    return "Importer: Reference Original: Path must be directory (cannot be a zip file)."
            if props.import_ref == "1":
                if props.copy_type == "1" and not source.path.is_dir():
                    return "Importer: Reference Project: Symlink: Path must be directory (cannot be a zip file)."

    else:
        if props.import_enabled:
            if props.import_ref == "0":
                return "Importer: Reference Original: Cannot be used with web or diffusion."

    return None
