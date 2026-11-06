"""Original schematic optics library. Run with Blender --background --python this_file."""
import bpy, math, json, os, sys
from mathutils import Vector
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
MAT = {}; ASSETS = []; CURRENT = None

def material(name, color, metal=0, rough=.3, transmission=0, ior=1.46, emission=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    for k,v in {'Base Color':(*color,1),'Metallic':metal,'Roughness':rough,'Transmission Weight':transmission,'IOR':ior}.items(): p.inputs[k].default_value=v
    if emission: p.inputs['Emission Color'].default_value=(*color,1); p.inputs['Emission Strength'].default_value=emission
    MAT[name]=m; return m
material('Glass • neutral blue',(.86,.96,1),rough=.055,transmission=1)
material('Glass • violet plate',(.73,.51,.94),rough=.08,transmission=.93)
material('Aluminum • satin',(.48,.54,.60),metal=1,rough=.29)
material('Aluminum • polished edge',(.77,.82,.86),metal=1,rough=.13)
material('Housing • graphite',(.035,.047,.06),metal=.65,rough=.32)
material('Recess • black',(.008,.012,.019),rough=.42)
material('Mirror • silver',(.94,.96,.98),metal=1,rough=.055)
material('Coating • splitter',(.56,.85,.91),metal=.25,rough=.09,transmission=.65)
material('Sensor • teal',(.025,.28,.32),metal=.5,rough=.18)
material('SLM • silicon',(.17,.12,.24),metal=.8,rough=.17)
material('Accent • teal',(.035,.49,.49),metal=.3,rough=.24)
material('Accent • amber',(.94,.40,.055),metal=.25,rough=.28)
material('Beam • amber', (1,.22,.025),rough=.25,emission=3)
material('Display • porcelain',(.72,.78,.81),rough=.4)
material('Ground • pale',(.86,.89,.91),rough=.5)
material('Typography • ink',(.024,.05,.075),rough=.7)
material('Indicator • mint',(.05,.8,.39),rough=.2,emission=1.5)

def link(obj,name,mat):
    obj.name=name
    for c in list(obj.users_collection): c.objects.unlink(obj)
    CURRENT.objects.link(obj)
    if mat: obj.data.materials.append(MAT[mat])
    return obj

def finish(obj, bevel=0):
    if bevel:
        b=obj.modifiers.new('Small manufactured edge','BEVEL'); b.width=bevel; b.segments=3
        n=obj.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return obj

def box(name,loc,size,mat,bevel=.04):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=link(bpy.context.object,name,mat)
    o.dimensions=size; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(o,bevel)

def cyl(name,loc,r,depth,mat,vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc,rotation=(math.pi/2,0,0))
    o=link(bpy.context.object,name,mat)
    for p in o.data.polygons: p.use_smooth=len(p.vertices)==4
    return finish(o,.018)

def ring(name,y,outer,inner,depth,mat):
    vs=[]; fs=[]; n=96
    for yy,rr in [(y-depth/2,outer),(y+depth/2,outer),(y-depth/2,inner),(y+depth/2,inner)]:
        vs += [(rr*math.cos(2*math.pi*i/n),yy,rr*math.sin(2*math.pi*i/n)) for i in range(n)]
    for i in range(n):
        j=(i+1)%n
        fs += [(i,j,n+j,n+i),(2*n+j,2*n+i,3*n+i,3*n+j),(j,i,2*n+i,2*n+j),(n+i,n+j,3*n+j,3*n+i)]
    me=bpy.data.meshes.new(name); me.from_pydata(vs,[],fs); me.update()
    o=bpy.data.objects.new(name,me); CURRENT.objects.link(o); me.materials.append(MAT[mat])
    for p in me.polygons: p.use_smooth=p.index%4<2
    return finish(o,.012)

def text(name,body,loc,size=.22,mat='Typography • ink',rot=(0,0,0),align='CENTER'):
    cu=bpy.data.curves.new(name,'FONT'); cu.body=body; cu.size=size; cu.align_x=align; cu.extrude=.001
    o=bpy.data.objects.new(name,cu); CURRENT.objects.link(o); o.location=loc; o.rotation_euler=rot; cu.materials.append(MAT[mat]); return o

def asset(key,title,description,params):
    global CURRENT
    CURRENT=bpy.data.collections.new('SO_'+key)
    bpy.context.scene.collection.children.link(CURRENT)
    CURRENT.asset_mark(); CURRENT.asset_data.description=description
    CURRENT.asset_data.author='Bllas / Schematic Optics'
    CURRENT.asset_data.catalog_id='31853180-7fbc-4aa8-87fb-d36618104c82'
    for tag in ['Schematic Optics','Optical component','v0.1']: CURRENT.asset_data.tags.new(tag)
    CURRENT['optical_axis']='+Y'; CURRENT['origin']='Optical center'; CURRENT['units']='1 Blender unit = 10 mm'; CURRENT['parameters']=json.dumps(params)
    ASSETS.append(dict(key=key,title=title,description=description,parameters=params,collection=CURRENT.name))
    return CURRENT

def screws(x,z,y):
    for xx in [-x,x]:
        for zz in [-z,z]:
            cyl('Recessed fastener',(xx,y,zz),.065,.025,'Aluminum • satin',32)
            box('Fastener slot',(xx,y-.018,zz),(.065,.008,.012),'Recess • black',.002)

def lens(key,title,kind):
    a=1.13; edge=.16; sag=.30; radial=28; n=128
    asset(key,title,'Smooth rotational lens with readable edge thickness; illustrative curvature, not a specified focal length.',dict(radius=a,edge_thickness=edge,sag=sag,profile=kind))
    # Each surface is a spherical cap; outward normals are recalculated below.
    R=(a*a+sag*sag)/(2*sag)
    def s(r): return math.sqrt(R*R-r*r)-math.sqrt(R*R-a*a)
    def yy(r,front):
        if kind=='biconvex': return (-edge/2-s(r)) if front else (edge/2+s(r))
        if kind=='plano_convex': return -edge/2-s(r) if front else edge/2
        return -(edge/2+sag)+s(r) if front else edge/2
    vs=[]; fs=[]
    for front in [True,False]:
        vs.append((0,yy(0,front),0))
        for j in range(1,radial+1):
            r=a*j/radial
            vs += [(r*math.cos(i*2*math.pi/n),yy(r,front),r*math.sin(i*2*math.pi/n)) for i in range(n)]
    stride=1+radial*n
    for side in range(2):
        off=side*stride
        for i in range(n): fs.append((off,off+1+i,off+1+(i+1)%n))
        for j in range(radial-1):
            b=off+1+j*n
            for i in range(n): q=(i+1)%n; fs.append((b+i,b+q,b+n+q,b+n+i))
    for i in range(n):
        q=(i+1)%n; b=1+(radial-1)*n; fs.append((b+i,b+q,b+stride+q,b+stride+i))
    me=bpy.data.meshes.new(title); me.from_pydata(vs,[],fs); me.update(); o=bpy.data.objects.new(title,me); CURRENT.objects.link(o); me.materials.append(MAT['Glass • neutral blue'])
    bpy.context.view_layer.objects.active=o; o.select_set(True)
    # Unlinked asset collections cannot enter edit mode; fix orientation with bmesh.
    import bmesh
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth=True
    o.select_set(False)


def scene(name):
    global CURRENT
    s=bpy.data.scenes.new(name); bpy.context.window.scene=s
    CURRENT=bpy.data.collections.new(name+' • presentation'); s.collection.children.link(CURRENT)
    s.unit_settings.system='METRIC'; s.unit_settings.scale_length=.01
    s.render.engine='CYCLES'; s.cycles.samples=48; s.cycles.use_denoising=True
    s.cycles.max_bounces=12; s.cycles.transmission_bounces=8
    s.render.resolution_x=1800; s.render.resolution_y=1500; s.render.resolution_percentage=100
    s.world=bpy.data.worlds.new(name+' • world'); s.world.use_nodes=True; s.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.74,.84,1); s.world.node_tree.nodes['Background'].inputs[1].default_value=.32
    s.view_settings.view_transform='AgX'
    return s

def instance(key,loc,angle=0):
    o=bpy.data.objects.new(key+' • instance',None); o.instance_type='COLLECTION'; o.instance_collection=bpy.data.collections['SO_'+key]; CURRENT.objects.link(o); o.location=loc; o.rotation_euler.z=angle; return o

def area(name,loc,power,size,target=(0,0,0),color=(1,1,1)):
    d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.shape='DISK'; d.size=size; d.color=color
    o=bpy.data.objects.new(name,d); CURRENT.objects.link(o); o.location=loc; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()

def camera(s,loc,target,scale):
    d=bpy.data.cameras.new(s.name+' Camera'); o=bpy.data.objects.new(s.name+' Camera',d); CURRENT.objects.link(o); o.location=loc; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler(); d.type='ORTHO'; d.ortho_scale=scale; d.lens=50; s.camera=o

def studio():
    box('Ground',(0,0,-.22),(200,200,.2),'Ground • pale',0)
    area('Key softbox',(-8,-10,16),2600,9)
    area('Long reflection',(9,3,13),3300,7)
    area('Front fill',(-1,-12,6),1000,6,color=(.8,.9,1))
