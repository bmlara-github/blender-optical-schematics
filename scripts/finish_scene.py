"""Camera-relative studio illumination and the approved translucent beam style.
Run after selecting a camera. Does not move optical components or the camera.
"""
import bpy
from mathutils import Vector

def finish_scene(scene, target=(-3, 0, 1.6), key_power=3300, fill_power=1100,
                 rim_power=2200, world_strength=.25, restore_beams=True):
    camera=scene.camera
    if camera is None: raise ValueError('Select a camera first')
    target=Vector(target)
    basis=camera.matrix_world.to_quaternion()
    right=basis @ Vector((1,0,0));up=basis @ Vector((0,1,0));front=basis @ Vector((0,0,1))
    # Reuse this rig on repeated calls and mute older scene lights.
    for obj in scene.objects:
        if obj.type=='LIGHT':obj.hide_render=True
    collection=bpy.data.collections.get('Camera studio')
    if collection is None:
        collection=bpy.data.collections.new('Camera studio');scene.collection.children.link(collection)
    settings=[('Key',(-12,14,18),key_power,11),
              ('Fill',(14,5,12),fill_power,12),
              ('Rim',(4,12,-10),rim_power,8)]
    for name,(x,y,z),power,size in settings:
        name='Camera studio '+name
        obj=bpy.data.objects.get(name)
        if obj is None:
            obj=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));collection.objects.link(obj)
        obj.hide_render=False;obj.data.energy=power;obj.data.shape='DISK';obj.data.size=size
        obj.location=target+x*right+y*up+z*front
        obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler()
        obj.data.use_shadow=True
    if scene.world is None:scene.world=bpy.data.worlds.new('Studio world')
    scene.world.use_nodes=True
    bg=scene.world.node_tree.nodes.get('Background')
    bg.inputs['Color'].default_value=(.8,.85,.9,1);bg.inputs['Strength'].default_value=world_strength
    if restore_beams:
        # Restore the exact transparent/emission mix used in the local envelope tests.
        for obj in scene.objects:
            if obj.type!='MESH' or not obj.get('model','').startswith('Illustrative quadratic'):continue
            rejected=any(t in obj.name.lower() for t in ['upper','zero','rejected'])
            for material in obj.data.materials:
                if not material or not material.use_nodes:continue
                nodes=material.node_tree.nodes
                emission=next((n for n in nodes if n.type=='EMISSION'),None)
                mix=next((n for n in nodes if n.type=='MIX_SHADER'),None)
                output=next((n for n in nodes if n.type=='OUTPUT_MATERIAL'),None)
                if emission and mix and output:
                    emission.inputs[0].default_value=(1,.008,.003,1)
                    emission.inputs[1].default_value=.336 if rejected else .7
                    mix.inputs[0].default_value=.14 if rejected else .21
                    material.node_tree.links.new(mix.outputs[0],output.inputs['Surface'])
            obj.visible_shadow=False
        # Recover center lines from the retained original volume endpoints.
        from beam_envelope import create_beam_core
        cores=bpy.data.collections.get('Publication beam cores')
        if cores is None:
            cores=bpy.data.collections.new('Publication beam cores');scene.collection.children.link(cores)
        for obj in list(scene.objects):
            if obj.type!='MESH' or not obj.get('schematic_envelope'):continue
            name=obj.name+' restored core'
            if bpy.data.objects.get(name):continue
            zs=[v.co.z for v in obj.data.vertices]
            a=obj.matrix_world @ Vector((0,0,min(zs)))
            b=obj.matrix_world @ Vector((0,0,max(zs)))
            rejected=any(t in obj.name.lower() for t in ['upper','zero','rejected'])
            radius=min(.018 if rejected else .026, .8*min(obj['radius_start_BU'],obj['radius_end_BU']))
            create_beam_core(name,a,b,cores,rejected,radius)
    scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='AgX'
    scene.render.engine='CYCLES';scene.cycles.use_denoising=True
    scene.cycles.max_bounces=12;scene.cycles.transparent_max_bounces=16
    bpy.context.view_layer.update()
    return {'target':list(target),'key_W':key_power,'fill_W':fill_power,'rim_W':rim_power,
            'world_strength':world_strength,'beam_style':'approved transparent envelope mix' if restore_beams else 'preserved from source scene',
            'lighting_frame':'camera right/up/front; schematic Blender units'}
