"""Reusable Gaussian volume beam builder; widths are illustrative 1/e^2 radii."""
import bpy
from mathutils import Vector

def create_gaussian_segment(name,start,end,wa,wb,collection,optical_height=0,rejected=False):
    a=Vector((start[0],start[1],optical_height)); b=Vector((end[0],end[1],optical_height)); length=(b-a).length
    limit=max(wa,wb)*2.5
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=limit,depth=length,location=(a+b)/2)
    o=bpy.context.object; o.name=name
    for c in list(o.users_collection): c.objects.unlink(o)
    collection.objects.link(o)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
    o.visible_shadow=False; o.visible_glossy=False
    m=bpy.data.materials.new(name+' • Gaussian volume'); m.use_nodes=True
    ns=m.node_tree.nodes; ns.clear(); links=m.node_tree.links
    def calc(op,a,b=None):
        n=ns.new('ShaderNodeMath'); n.operation=op
        for i,v in enumerate([a,b]):
            if v is None: continue
            if isinstance(v,(int,float)): n.inputs[i].default_value=v
            else: links.new(v,n.inputs[i])
        return n.outputs[0]
    coord=ns.new('ShaderNodeTexCoord'); sep=ns.new('ShaderNodeSeparateXYZ'); links.new(coord.outputs['Generated'],sep.inputs[0])
    x=calc('MULTIPLY',calc('SUBTRACT',sep.outputs['X'],.5),2*limit)
    y=calc('MULTIPLY',calc('SUBTRACT',sep.outputs['Y'],.5),2*limit)
    r2=calc('ADD',calc('MULTIPLY',x,x),calc('MULTIPLY',y,y))
    # Smooth quadratic waist law along each authored optical segment.
    t=sep.outputs['Z'] if wb>=wa else calc('SUBTRACT',1,sep.outputs['Z'])
    w2=calc('ADD',min(wa,wb)**2,calc('MULTIPLY',calc('MULTIPLY',t,t),abs(wb*wb-wa*wa)))
    gaussian=calc('EXPONENT',calc('MULTIPLY',-2,calc('DIVIDE',r2,w2)))
    vol=ns.new('ShaderNodeVolumePrincipled'); vol.inputs['Color'].default_value=(.9,.08,.025,1)
    links.new(calc('MULTIPLY',gaussian,.04),vol.inputs['Density'])
    # Normalize apparent brightness across narrow waists for diagram readability.
    strength=calc('DIVIDE',1.1 if rejected else 3.5,calc('SQRT',w2))
    links.new(calc('MULTIPLY',gaussian,strength),vol.inputs['Emission Strength'])
    vol.inputs['Emission Color'].default_value=(1,.035,.008,1)
    out=ns.new('ShaderNodeOutputMaterial'); links.new(vol.outputs['Volume'],out.inputs['Volume']); o.data.materials.append(m)
    o['profile']='I(r,z) proportional to exp(-2*r^2/w(z)^2)'; o['radius_start_BU']=wa; o['radius_end_BU']=wb; o['schematic_envelope']=True
    return o
