# Optional search for a compact camera view

Use this workflow when a schematic has excessive empty space. It is optional: preserve an accepted POV unless the user asks to explore alternatives. The compact preset is one useful starting point, not an optimum for every optical layout. This workflow applies to the schematic project; it does not change the experimental project's accepted camera.

## Ask the agent

> Search for a more compact orthographic POV for this schematic. Keep the optical geometry, component instances and focal spans fixed. Preserve the original figure. Compare a coarse grid of azimuths and elevations, then refine near promising views. Re-anchor the camera-facing CCD and SLM reference panels for every candidate. Rank unclipped views by approximate empty page area at 86 mm width, but reject views that obscure optical faces, merge beam branches or leave insufficient room for readable labels. Show a comparison and save the selected camera as a reusable preset. Export matching lettered and unlettered SVGs with 0.5 mm borders. Close any application windows opened for this task when finished.

## Render and compare

Work in a new `Figures/YYYY-MM-DD-FIgNN/` directory using the user's local date. Save the current figure before starting. Render transparent previews with fixed geometry, panel size, camera scale, resolution and lighting; change only the viewing direction and necessary camera-facing panel placement. Do not compare a clipped render with a complete render.

Inside Blender, import `render_camera_candidates` from `scripts/search_camera_views.py`:

```python
from search_camera_views import render_camera_candidates
render_camera_candidates(
    bpy.context.scene, '/path/to/new-figure/coarse',
    target=(-3, 0, 1.6),
    azimuths=[-110, -90, -70], elevations=[30, 45, 60],
    ortho_scale=44, distance=60,
    update_panels=update_reference_panels)
```

Substitute scene-appropriate coordinates and define `update_reference_panels(scene, camera)` using the existing panel placement helper. This callback is required when the figure has reference panels; omit it only for scenes without panels. Recalculate their camera-parallel orientation, silhouette clearance and lower-corner anchors at every angle. Reuse the figure's existing panel objects. The function restores the original camera, object transforms and render settings after the sweep, including on failure. It does not save over the Blender file or select a winner. The output directory must be new.

For the standard object names, a panel callback can be defined as follows. Change the object names to match your scene:

```python
from panel_layout import housing_corner, silhouette_edge, place_panel

def update_reference_panels(scene, camera):
    items = [
        ('CCD', 'CCD intensity', 'Reference frame',
         'Camera housing', 'rear', 'left'),
        ('SLM', 'SLM hologram', 'SLM reference frame',
         'SLM housing', 'front', 'right')]
    for instrument, image, frame, prefix, face, side in items:
        obj = bpy.data.objects[instrument]
        anchor = housing_corner(scene, camera, obj, prefix, face, side)
        place_panel(scene, camera, bpy.data.objects[image],
                    bpy.data.objects[frame], anchor, side, .012,
                    width=3.4,
                    edge_u=silhouette_edge(scene, camera, obj, side))
```

The sample panel width and gap follow the schematic example. Keep your figure's own accepted values when they differ. Add the project's `scripts/` directory to Python's import path before importing the helpers.

Azimuth is measured from world +X toward +Y; elevation is measured above the XY plane. The example distances are schematic Blender units, not millimetres. Adjust camera scale and canvas dimensions if any candidate is clipped, then rerun the entire comparison with consistent framing.

Outside Blender, with Python and Pillow:

```sh
python scripts/rank_camera_views.py /path/to/new-figure/coarse
```

This creates `comparison.png` and `ranked.json`. Each candidate already has its own PNG and reusable camera JSON. Defaults are 86 mm page width and 0.5 mm borders; use `--width-mm` and `--border-mm` to override them.

The measurements are cropped page height, alpha-mask occupied fraction and approximate empty page area. The ranking uses empty page area, not height alone. Alpha coverage is only a proxy: glass and translucent beams make its numerical value threshold-dependent. A compact but unreadable view is not a valid choice. Reject edge-on apertures, hidden SLM faces, overlapping components, indistinguishable beam branches and cropped image panels. Add the final lettering before accepting the composition.

Refine promising angles with a smaller grid. The [single worked example](../examples/paper-setup/README.md) and [user guide](user-guide.pdf) use the original paper setup for both the nine-view coarse sampler and six-view refinement. The -75 degree / 25 degree preset is demonstrated as an alternative; it shows the back of the SLM and is unsuitable when the active face must be visible. Compare the supplied fixed view before accepting it. No global minimum is claimed.

## Apply and export

Use `apply_camera_preset(scene, preset_path)` from `scripts/camera_presets.py` to apply the selected candidate. The included starting point is:

`library/camera-presets/folded-relay-compact-oblique.json`

Its name is **Folded Relay — Compact Oblique**. Re-anchor panels after applying it. Render the selected scene at final quality, place readable vector lettering, and check that all content fits. Export two SVGs at the requested width with explicit millimetre dimensions and equal requested borders. Embed the raster optical render without aspect distortion; retain lettering in a separate editable vector layer.

Keep the selected Blender file, camera JSON, source images, render, comparison, measurements, SVG pair and notes together. Record why the chosen view won and any readability tradeoff. Preserve the original figure and preset. If Blender is opened to run the scripts, save the result and close that window when done.
