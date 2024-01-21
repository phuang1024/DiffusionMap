import os
from pathlib import Path

import bpy

from .execute import Asset, Catalog, CatalogType, execute_main, validate_settings, get_source
from .icons import *


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


class DMAP_OT_TexlistRefresh(bpy.types.Operator):
    """Refresh the texture list."""
    bl_idname = "dmap.texlist_refresh"
    bl_label = "Refresh"
    bl_options = {"REGISTER"}

    def execute(self, context):
        props = context.scene.dmap
        prefs = context.preferences.addons[__package__].preferences

        props.texlist.clear()

        if props.source == "0":
            raise ValueError("Cannot search texlist on local file source.")

        elif props.source == "1":
            catalog = Catalog(CatalogType.GLOBAL, bpy.path.abspath(prefs.catalog_path))
            results = catalog.iter_textures()

        elif props.source == "2":
            raise NotImplementedError("Web search not implemented yet.")

        elif props.source == "3":
            raise NotImplementedError("Diffusion not implemented yet.")

        else:
            raise RuntimeError("This should never happen.")

        clear_icons("texlist")

        for id in sorted(results.keys()):
            # Compile res and path strings.
            res = ""
            paths = ""
            for r, p in results[id].items():
                res += f"{r} "
                paths += f"{p}{os.path.pathsep}"
            res = res.strip()
            paths = paths.strip(os.path.pathsep)

            # Search for icon
            icon = None
            for r, p in results[id].items():
                asset = Asset(p)
                maps = asset.get_maps()
                if "preview" in maps:
                    icon = maps["preview"]
                    break

            if icon is not None:
                load_icon("texlist", id, str(icon))

            p = props.texlist.add()
            p.id = id
            p.res = res
            p.path = paths

        return {"FINISHED"}


class DMAP_OT_WebSearch(bpy.types.Operator):
    """Search for textures on AmbientCG."""
    bl_idname = "dmap.web_search"
    bl_label = "Search"
    bl_options = {"REGISTER"}

    def execute(self, context):
        # TODO
        return {"FINISHED"}


class DMAP_OT_ExportSource(bpy.types.Operator):
    # TODO when the fileselector appears, it selects a directory but looks like it selects a file. Maybe blender bug?
    """Export the source texture to a local file."""
    bl_idname = "dmap.export_source"
    bl_label = "Export to file"
    bl_options = {"REGISTER"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        source = get_source(context)
        export_path = source.export(Path(self.directory))
        self.report({"INFO"}, f"Exported to {export_path}")
        return {"FINISHED"}
