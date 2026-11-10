# Original example with camera-relative studio illumination

Original nine-component paper setup; original SLM and CCD images. Both accepted camera transforms are preserved. Three area lights follow the camera frame. Existing flat beam override is replaced by the translucent envelope and thin shaded core from the local tests. Rejected orders remain dimmer red. Widths and cores are schematic visualization, not diffraction simulation.

Run the guide through Step 11, then `workflow.finish('compact', OUT)` and optionally `workflow.finish('fixed', OUT)`. Export the `OUT/finished` directory with the example exporter. The final figures here are 86 mm wide, with 0.5 mm borders and editable vector lettering over raster optics. Local source copies and both Blender scenes are retained here.

Key (-12,14,18), fill (14,5,12), rim (4,12,-10), in camera right/up/front axes about target (-3,0,1.6). Powers 3300/1100/2200 W, sizes 11/12/8 BU, world strength .25, AgX, Cycles 64 samples and denoising. The compact direction still shows the back of the SLM; use fixed when its active face must be visible.
