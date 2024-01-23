import os
from pathlib import Path

import bpy
import requests

from .catalog import get_name_res
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

        if props.source == "0":
            raise ValueError("Cannot search texlist on local file source.")

        elif props.source == "1":
            catalog = Catalog(CatalogType.GLOBAL, bpy.path.abspath(prefs.catalog_path))
            results = catalog.iter_textures()

        elif props.source == "2":
            return {"CANCELLED"}
            #raise NotImplementedError("Web search not implemented yet.")

        elif props.source == "3":
            raise NotImplementedError("Diffusion not implemented yet.")

        else:
            raise RuntimeError("This should never happen.")

        props.texlist.clear()
        clear_icons("texlist")

        for id in sorted(results.keys()):
            # Compile res and path strings.
            res = ""
            paths = ""
            for r, p in results[id].items():
                res += f"{r} "
                paths += f"{p};"
            res = res.strip()
            paths = paths.strip(";")

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
        def query_acg(query: str, count: int, offset: int) -> dict:
            r = requests.get(
                "https://ambientcg.com/api/v2/full_json?"
                "type=Material&"
                "sort=Latest&"
                "include=downloadData,mapData&"
                f"limit={count}&"
                f"offset={offset}&"
                f"q={query}&"
                "method=PBRApproximated,PBRPhotogrammetry,PBRProcedural,PBRMultiAngle"
            )
            r.raise_for_status()
            return r.json()

        props = context.scene.dmap

        props.texlist.clear()

        results = query_acg(props.web_query, props.web_limit, 0)
        for asset in results["foundAssets"]:
            p = props.texlist.add()
            p.id = asset["assetId"]

            res_options = {}
            for download in asset["downloadFolders"]["default"]["downloadFiletypeCategories"]["zip"]["downloads"]:
                if "jpg" in download["attribute"].lower():
                    _, res = get_name_res(download["fileName"])
                    res_options[res] = download["downloadLink"]

            res_str = ""
            path_str = ""
            for key in sorted(res_options.keys()):
                res_str += f"{key} "
                path_str += f"{res_options[key]};"
            res_str = res_str.strip()
            path_str = path_str.strip(";")

            p.res = res_str
            p.path = path_str

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
        source = get_source(context, execute=True)
        export_path = source.export(Path(self.directory))
        self.report({"INFO"}, f"Exported to {export_path}")
        return {"FINISHED"}
