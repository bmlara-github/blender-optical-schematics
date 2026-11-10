"""Optional orthographic camera sweep. Run inside Blender; inspect before selecting."""
import json
import math
from pathlib import Path
import bpy
from mathutils import Vector


def render_camera_candidates(scene, output_dir, *, target, azimuths, elevations,
                             ortho_scale, distance=None, resolution=(1000, 800),
                             samples=16, update_panels=None):
    """Render candidates into a NEW directory, then restore the working scene.

    Angles are degrees: azimuth from +X toward +Y, elevation above XY.
    Geometry stays fixed. update_panels(scene, camera) must re-anchor any
    camera-facing reference panels using the project's panel conventions.
    No winning view is applied automatically. Use rank_camera_views.py next.
    """
    cam = scene.camera
    if cam is None or cam.data.type != 'ORTHO':
        raise ValueError('Select an orthographic scene camera first')
    target = Vector(target)
    distance = (cam.location-target).length if distance is None else distance
    azimuths, elevations = list(azimuths), list(elevations)
    if not azimuths or not elevations or distance <= 0 or ortho_scale <= 0:
        raise ValueError('Supply nonempty angle lists and positive framing distances')
    if any(not -89 < e < 89 for e in elevations):
        raise ValueError('Elevations must lie strictly between -89 and 89 degrees')
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    # Also restore panel transforms changed by the callback, including frame scale.
    transforms = [(o, o.matrix_world.copy()) for o in scene.objects]
    rotation_mode = cam.rotation_mode
    scale = cam.data.ortho_scale
    render_keys = ['resolution_x','resolution_y','resolution_percentage','filepath',
                   'film_transparent','pixel_aspect_x','pixel_aspect_y']
    old_render = {k:getattr(scene.render,k) for k in render_keys}
    old_format = (scene.render.image_settings.file_format, scene.render.image_settings.color_mode)
    old_samples = scene.cycles.samples
    rows = []
    try:
        scene.render.resolution_x, scene.render.resolution_y = resolution
        scene.render.resolution_percentage = 100
        scene.render.pixel_aspect_x = scene.render.pixel_aspect_y = 1
        scene.render.film_transparent = True
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'
        scene.cycles.samples = samples
        cam.rotation_mode = 'XYZ'
        cam.data.ortho_scale = ortho_scale
        for az in azimuths:
            for el in elevations:
                a,e = math.radians(az),math.radians(el)
                offset = Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)))*distance
                cam.location = target + offset
                cam.rotation_euler = (-offset).to_track_quat('-Z','Y').to_euler()
                bpy.context.view_layer.update()
                if update_panels is not None:
                    update_panels(scene,cam)
                    bpy.context.view_layer.update()
                name = f'view_{len(rows):03d}'
                scene.render.filepath = str(out/(name+'.png'))
                bpy.ops.render.render(write_still=True)
                preset = dict(schema_version=1,id=name,name=f'Az {az:g}, elevation {el:g}',
                    projection='ORTHO',location=list(cam.location),
                    rotation_euler_xyz_radians=list(cam.rotation_euler),
                    rotation_quaternion_wxyz=list(cam.rotation_euler.to_quaternion()),
                    target=list(target),offset_from_target=list(offset),
                    orthographic_scale=ortho_scale,lens_mm=cam.data.lens,
                    clip_start=cam.data.clip_start,clip_end=cam.data.clip_end,
                    reference_meters_per_blender_unit=scene.unit_settings.scale_length,
                    resolution=list(resolution),pixel_aspect=[1,1],
                    azimuth_deg=az,elevation_deg=el)
                (out/(name+'.json')).write_text(json.dumps(preset,indent=2)+'\n')
                rows.append(dict(id=name,image=name+'.png',preset=name+'.json',azimuth_deg=az,elevation_deg=el))
                (out/'candidates.json').write_text(json.dumps(rows,indent=2)+'\n')
    finally:
        cam.rotation_mode = rotation_mode
        for obj,matrix in transforms:
            obj.matrix_world = matrix
        cam.data.ortho_scale = scale
        for k,v in old_render.items(): setattr(scene.render,k,v)
        scene.render.image_settings.file_format,scene.render.image_settings.color_mode = old_format
        scene.cycles.samples = old_samples
        bpy.context.view_layer.update()
    return rows
