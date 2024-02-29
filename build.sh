#!/bin/bash

# Make a zip file for the Blender add-on.

mkdir -p build

cp -r src/Blender build/diffusionmap
# Replace symlink with real files.
rm build/diffusionmap/ColorDiffusion
cp -r src/ColorDiffusion build/diffusionmap/

cd build
zip -r DiffusionMap.zip diffusionmap
