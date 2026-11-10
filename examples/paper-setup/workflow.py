"""One scene for the fixed POV, coarse/refined search, and selected POV.

Blender console:
    import sys
    sys.path.insert(0, '/path/to/project/examples/paper-setup')
    import workflow
    workflow.run('fixed', 'Figures/2026-11-10-FIg01')

CLI: blender --background --python examples/paper-setup/workflow.py -- fixed --output Figures/2026-11-10-FIg01
"""
from pathlib import Path
import sys,json,argparse
import bpy
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from camera_presets import apply_camera_preset
from panel_layout import housing_corner,silhouette_edge,place_panel
from search_camera_views import render_camera_candidates


def update_reference_panels(scene,camera):
    """Reuse the same two image panels; retain the established corner convention."""
    checks=[]
    for n,pn,fn,prefix,face,side in [
        ('CCD','CCD intensity','Reference frame','Camera housing','rear','left'),
        ('SLM','SLM hologram','SLM reference frame','SLM housing','front','right')]:
        obj=bpy.data.objects[n]
        anchor=housing_corner(scene,camera,obj,prefix,face,side)
        checks.append(place_panel(scene,camera,bpy.data.objects[pn],
            bpy.data.objects[fn],anchor,side,.012,width=3.4,
            edge_u=silhouette_edge(scene,camera,obj,side)))
    bpy.context.view_layer.update()
    return checks


def load_example():
    """Open the bundled scene. Save any unrelated open work before calling."""
    bpy.ops.wm.open_mainfile(filepath=str(HERE/'source.blend'),load_ui=False)
    # Reload the two supplied inputs so replacing their copies is sufficient.
    for object_name,file in [('CCD intensity','ccd_intensity.png'),('SLM hologram','slm_hologram.png')]:
        obj=bpy.data.objects[object_name]
        node=next(n for n in obj.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE')
        node.image=bpy.data.images.load(str(HERE/'reference-images'/file),check_existing=False)
        node.image.pack()
    return bpy.context.scene


def run(stage,output):
    """stage is fixed, coarse, refine, or compact; output is relative to root."""
    if stage not in ['fixed','coarse','refine','compact']:
        raise ValueError('Stage must be fixed, coarse, refine, or compact')
    out=Path(output)
    if not out.is_absolute():out=ROOT/out
    out.mkdir(parents=True,exist_ok=True)
    if stage in ['fixed','compact'] and (out/(stage+'.blend')).exists():
        raise FileExistsError('Preserve prior results: choose a new output folder')
    scene=load_example()
    preset=ROOT/'library/camera-presets'/('folded-relay-compact-oblique.json' if stage=='compact' else 'folded-relay-front-left.json')
    camera=apply_camera_preset(scene,preset,ortho_scale=44,resolution=(2400,1800))
    checks=update_reference_panels(scene,camera)
    if stage in ['coarse','refine']:
        return render_camera_candidates(scene,out/stage,target=(-3,0,1.6),
            azimuths=[-110,-90,-70] if stage=='coarse' else [-105,-75],
            elevations=[30,45,60] if stage=='coarse' else [15,25,35],
            ortho_scale=44,distance=60,resolution=(1000,800),samples=16,
            update_panels=update_reference_panels)
    (out/'renders').mkdir(exist_ok=True)
    scene.cycles.samples=64
    scene.render.filepath=str(out/'renders'/(stage+'.png'))
    anchors=[]
    for name in ['Laser','P','L1P','L2P','SLM','L2','SF','L1','CCD']:
        p=world_to_camera_view(scene,camera,bpy.data.objects[name].location)
        anchors.append(dict(name=name,x=p.x*scene.render.resolution_x,
                            y=(1-p.y)*scene.render.resolution_y))
    (out/(stage+'-anchors.json')).write_text(json.dumps(anchors,indent=2))
    (out/(stage+'-panels.json')).write_text(json.dumps(checks,indent=2))
    camera_record=json.loads(preset.read_text())
    camera_record['orthographic_scale']=camera.data.ortho_scale
    camera_record['resolution']=[scene.render.resolution_x,scene.render.resolution_y]
    (out/(stage+'-camera.json')).write_text(json.dumps(camera_record,indent=2))
    bpy.ops.wm.save_as_mainfile(filepath=str(out/(stage+'.blend')))
    bpy.ops.render.render(write_still=True)
    return str(out)

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('stage',choices=['fixed','coarse','refine','compact']);p.add_argument('--output',required=True)
    a=p.parse_args(args);run(a.stage,a.output)
