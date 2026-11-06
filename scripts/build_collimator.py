import bpy, math, json, sys, base64
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
helper=ROOT/'scripts/collimator_primitives.py'
ns={'__file__':str(helper)}
exec(compile(helper.read_text(),str(helper),'exec'),ns)
ns['lens']('Collimator','Optical collimator','plano_convex')
a=ns['CURRENT']; a.asset_data.description='Generic mounted optical collimator: rear input, recessed positive lens, output along local -Y. Focal length belongs to scene metadata.'
a.asset_data.author='B. M. Rodriguez-Lara'
for o in list(a.objects):
    for v in o.data.vertices: v.co*=.62; v.co.y+=.22
ring=ns['ring']
ring('Graphite hollow barrel',1.0,.86,.72,1.9,'Housing • graphite')
ring('Satin front collar',.08,.91,.71,.22,'Aluminum • satin')
ring('Front retaining ring',-.04,.75,.65,.08,'Housing • graphite')
ring('Rear coupling',2.02,.64,.22,.35,'Aluminum • satin')
ring('Rear input rim',2.22,.36,.18,.09,'Housing • graphite')
ring('Teal identification band',1.58,.875,.85,.06,'Accent • teal')
for i in range(4): ring('Focus collar groove',.56+i*.1,.874,.85,.025,'Aluminum • satin')
a['optical_axis']='Y'; a['output_direction']='-Y'; a['origin']='Output aperture center'; a['parameters']=json.dumps({'type':'generic mounted positive-lens collimator','focal_length':'scene-defined','geometry':'illustrative','output_aperture_diameter_BU':1.3})
a['input_port_local']=[0,2.265,0]; a['output_port_local']=[0,-.08,0]
a.asset_data.tags.new('Collimator')
fig=ROOT/'Figures/2026-11-06-FIg01'; (fig/'renders').mkdir(parents=True,exist_ok=True); (fig/'svg').mkdir(exist_ok=True)
s=ns['scene']('Collimator • schematic preview'); s.render.resolution_x=1800;s.render.resolution_y=1200
s.cycles.samples=48
ns['instance']('Collimator',(0,1,1.2))
ns['studio'](); ns['area']('Key',(2,-4,9),1600,7);ns['area']('Rim',(-5,3,6),1300,5);ns['area']('Fill',(6,5,5),900,4)
ns['camera'](s,(9,-11,8),(0,-1,1),9.5)
sys.path.insert(0,str(ROOT/'scripts')); from gaussian_beam import create_gaussian_segment
create_gaussian_segment('Collimated output',(0,.90),(0,-5),.28,.28,ns['CURRENT'],optical_height=1.2)
# Strengthen the illustrative beam against the pale presentation background.
beam=bpy.data.objects['Collimated output']
for node in beam.data.materials[0].node_tree.nodes:
    if node.type=='MATH' and node.operation=='DIVIDE' and not node.inputs[0].is_linked and abs(node.inputs[0].default_value-3.5)<.001:
        node.inputs[0].default_value=21.0
# Canonical asset geometry is only instanced in the presentation scene.
for sc in list(bpy.data.scenes):
    if sc!=s: bpy.data.scenes.remove(sc)
s.render.filepath=str(fig/'renders/collimator_unlettered.png')
report={'asset':'SO_Collimator','library_file':'Bllas_Schematic_Optics_Additions_v04.blend','units':'1 BU = 10 mm','origin':'Output aperture center','output_axis':'-Y','focal_length':'scene-defined','materials':[m.name for m in bpy.data.materials if m.users],'checks':{'asset_marked':bool(a.asset_data),'no_lettering':not any(o.type=='FONT' for o in s.objects),'no_arrows':not any('arrow' in o.name.lower() for o in s.objects),'lens_present':any('collimator' in o.name.lower() for o in a.objects)}}
(ROOT/'docs/asset_additions_v04.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'library/Bllas_Schematic_Optics_Additions_v04.blend'))
bpy.ops.wm.save_as_mainfile(filepath=str(fig/'2026-11-06-FIg01.blend'))
bpy.ops.render.render(write_still=True)
png=base64.b64encode((fig/'renders/collimator_unlettered.png').read_bytes()).decode()
for lettered in [False,True]:
    label='<g inkscape:groupmode="layer" inkscape:label="Editable lettering" id="labels"><text x="900" y="1100" text-anchor="middle" font-family="sans-serif" font-size="44" fill="#223440">Optical collimator</text></g>' if lettered else ''
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="86mm" height="57.333333mm" viewBox="0 0 1800 1200"><image width="1800" height="1200" href="data:image/png;base64,{png}"/>{label}</svg>'
    svg=svg.replace('http://www.inkscape.org/namespaces/inkscape','http://www.inkscape.org/namespaces/inkscape')
    (fig/'svg'/('collimator_'+('lettered' if lettered else 'unlettered')+'_86mm.svg')).write_text(svg)
print('COLLIMATOR_COMPLETE',json.dumps(report))
