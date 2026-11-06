Use $setup-to-blender to create a schematic reconstruction of the optical setup referenced by https://doi.org/10.1103/6ftp-svh8.

Read examples/paper-setup/README.md and layout.json. This is a later visualization; the paper did not use these Blender models.

Use Laser -> P (circular pupil) -> L1P -> L2P -> reflective SLM -> L2 -> SF (transmit +1 order) -> L1 -> CCD. Show rejected 0 and -1 orders stopping at SF. Preserve the supplied labels and document the known L1/L2 disagreement with manuscript prose. Do not add a polarizer or beam splitter.

Use only this repository's library collections. Treat the supplied layout as authored assumptions, not measured distances; focal lengths are unknown. Use the schematic asset scale and keep the layout illustrative. Use continuous red beams and dimmer same-hue rejected orders. Do not add arrows or cable-like connectors.

If I provide a lawful copy of the paper figure/sketch and reference PNGs, inspect them and place each supplied image near its instrument. Otherwise generate the documented topology without reference-image insets and record that no sketch/image comparison was performed. Do not invent experimental images.

Save under a new Figures/YYYY-MM-DD-FIgNN/ using my local date. Deliver an editable Blender file, reproducible build.py and setup.json, perspective/plan PNGs, paired lettered/unlettered SVGs at 86 mm, and notes separating facts, assumptions and checks. Render at 2000 x 1600 and 40 Cycles samples. Preserve the libraries and any existing figures.
