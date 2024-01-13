__all__ = (
    "download_data",
)

import time
import shutil
from pathlib import Path
from threading import Thread
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import requests

REQUIRED_MAPS = (
    "color",
    "displacement",
    "roughness",
)

BANNED_MAPS = (
    "opacity",
)

REQUIRED_RES = "1K-JPG"


def query_catalog(query: str, count: int, offset: int) -> dict:
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


def validate_asset(asset: dict) -> bool:
    """
    asset: Asset metadata json from AmbientCG API.
    """
    maps = asset["maps"]
    maps = [m.lower() for m in maps]

    for map_type in REQUIRED_MAPS:
        if map_type not in maps:
            return False

    for map_type in BANNED_MAPS:
        if map_type in maps:
            return False

    downloads = asset["downloadFolders"]["default"]["downloadFiletypeCategories"]["zip"]["downloads"]

    for download in downloads:
        if REQUIRED_RES.lower() in download["attribute"].lower():
            break
    else:
        return False

    return True


def download_asset(output_dir: Path, asset: dict):
    asset_path = output_dir / asset["assetId"]

    downloads = asset["downloadFolders"]["default"]["downloadFiletypeCategories"]["zip"]["downloads"]
    for download in downloads:
        if REQUIRED_RES.lower() in download["attribute"].lower():
            download_url = download["downloadLink"]
            break
    else:
        raise RuntimeError(f"No {REQUIRED_RES} download found for {asset['assetId']}.")

    r = requests.get(download_url)
    r.raise_for_status()

    with TemporaryDirectory() as tmp_dir:
        zip_path = Path(tmp_dir) / "asset.zip"
        with open(zip_path, "wb") as f:
            f.write(r.content)
        with ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(tmp_dir)

        asset_path.mkdir(parents=True, exist_ok=True)
        for map_type in REQUIRED_MAPS:
            for file in Path(tmp_dir).iterdir():
                if file.suffix.lower() == ".jpg" and map_type in file.stem.lower():
                    map_path = asset_path / f"{map_type}.jpg"
                    shutil.copy(file, map_path)
                    break
            else:
                raise RuntimeError(f"No {map_type} map found for {asset['assetId']}.")

    print(f"  {asset['assetId']} done.")


def download_data(output_dir: Path, search_query: str = "", count: int = 100, bs: int = 10, backoff: float = 1):
    """
    Download data from AmbientCG and save to ``output_dir``.

    Queries for the latest PBR assets (up to ``count``).
    Downloads 1K JPG.
    Saves in format specificed in docs.

    output_dir: Path to output directory.
    query: Query string for AmbientCG API.
    count: Number of assets to download.
    bs: Batch size for querying. One thread is started per asset in a batch.
    backoff: Backoff time between batches.
    """
    print(f"Downloading {count} assets to {output_dir}.")
    output_dir.mkdir(parents=True, exist_ok=True)

    offset = 0
    i = 0
    remaining = count
    done = 0
    while remaining > 0:
        query = query_catalog(search_query, bs, offset)
        assets = query["foundAssets"]
        if len(assets) == 0:
            break

        threads = []
        for asset in assets:
            if validate_asset(asset):
                thread = Thread(target=download_asset, args=(output_dir, asset))
                threads.append(thread)
                remaining -= 1
                done += 1
            if remaining <= 0:
                break

        print(f"Batch {i}:\t{len(threads)} validated;\t{done} done;\t{remaining} remaining.")

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        offset += bs
        i += 1

        time.sleep(backoff)
