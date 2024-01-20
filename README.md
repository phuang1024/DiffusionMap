# DiffusionMap

AI tools for Blender materials.

## ML model data storage format

```
data
|__ AssetName001
    |__ color.jpg
    |__ displacement.jpg
    |__ roughness.jpg
...
```

## Add-on data storage format

### Global catalog

e.g. `/path/to/Catalog/`

```
data
|__ AssetName001
    |__ 1         # 1K resolution
        |__ AssetName001_1K-JPG_Color.jpg
        ...
    ...
```

### Project

e.g. `/project/Textures/`

```
data
|__ AssetName001_1K
    |__ AssetName001_1K-JPG_Color.jpg
    ...
```
