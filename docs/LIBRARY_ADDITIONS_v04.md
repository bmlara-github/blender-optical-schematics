# Generic optical collimator

Added 6 November 2026. Asset: `SO_Collimator`, in `library/Bllas_Schematic_Optics_Additions_v04.blend`.

## Design
A compact hollow graphite barrel with satin aluminum front and rear collars, a recessed positive plano-convex glass lens, dark retaining rings, a restrained teal identification band and simplified focus-collar grooves. This is a generic mounted collimator, not manufacturer CAD. Rear input is a small axial opening; no cable is attached. The lens uses the existing generic positive-lens design and library glass material.

## Reuse and alignment
Append or instance the marked collection `SO_Collimator`. One Blender unit represents 10 mm. Origin is the center of the output aperture, local Y is the optical axis, output travels along -Y; rear input lies toward +Y. The preview beam is separate from the asset. Body dimensions are schematic, not a product specification. Focal length, wavelength, source position, beam diameter and residual divergence belong to scene metadata; do not create a new asset per focal length.

## Optical interpretation
The example represents an adjusted positive-lens collimator fed by a source near its front focal plane. Its external red beam has constant displayed width, indicating approximately collimated propagation over the illustrated span. It is a Gaussian-emission visualization, not a diffraction simulation or a claim of exactly zero Gaussian divergence. The enclosed source and internal ray propagation are not depicted. For cutaway or explanatory figures, place the source at the appropriate focal distance and preserve relative focal spans.

## Materials and presentation
Existing blue glass (IOR 1.46, transmission 1, roughness 0.055), graphite housing, satin aluminum, and teal accent materials are reused. Broad studio illumination reveals the cylindrical form and recessed optic. No directional arrows or connection cables are included.

## Outputs
The bundled preview and paired SVGs are linked from [examples/collimator](../examples/collimator/README.md). Rebuilding writes a Blender scene, PNG and SVGs to `Figures/2026-11-06-FIg01/`. SVGs embed the raster optical rendering; the lettered version adds editable vector text for Inkscape. The unlettered version contains no lettering. Build with `scripts/build_collimator.py` using Blender in background mode.
