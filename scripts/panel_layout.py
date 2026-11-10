"""Camera-space panel anchoring for orthographic and perspective cameras."""
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

def project(scene, camera, point):
    return world_to_camera_view(scene, camera, point)

def unproject(scene, camera, uv, depth):
    corners=camera.data.view_frame(scene=scene)
    xmin,xmax=min(p.x for p in corners),max(p.x for p in corners)
    ymin,ymax=min(p.y for p in corners),max(p.y for p in corners)
    k=depth/(-corners[0].z) if camera.data.type=='PERSP' else 1
    return camera.matrix_world @ Vector(((xmin+uv[0]*(xmax-xmin))*k,(ymin+uv[1]*(ymax-ymin))*k,-depth))

def housing_corner(scene, camera, instance, housing_prefix, face, side, vertical="bottom"):
    """Semantic front/rear face is local -Y/+Y; left/right is screen-relative."""
    body=next(o for o in instance.instance_collection.objects if o.name.startswith(housing_prefix))
    points=[Vector(p) for p in body.bound_box]
    yy=(min if face=='front' else max)(p.y for p in points)
    if vertical not in ("bottom", "top"): raise ValueError("vertical must be bottom or top")
    zz=(min if vertical=="bottom" else max)(p.z for p in points)
    world=[instance.matrix_world @ body.matrix_world @ p for p in points if abs(p.y-yy)<1e-5 and abs(p.z-zz)<1e-5]
    return (min if side=='left' else max)(world,key=lambda p:project(scene,camera,p).x)

def silhouette_edge(scene,camera,instance,side):
    """Projected extreme of evaluated mesh vertices, including bevels and protrusions."""
    depsgraph=bpy.context.evaluated_depsgraph_get();xs=[]
    for obj in instance.instance_collection.all_objects:
        if obj.type!='MESH' or obj.hide_render: continue
        evaluated=obj.evaluated_get(depsgraph);mesh=evaluated.to_mesh()
        transform=instance.matrix_world @ evaluated.matrix_world
        xs.extend(project(scene,camera,transform @ v.co).x for v in mesh.vertices)
        evaluated.to_mesh_clear()
    if not xs: raise ValueError('No renderable mesh in instrument collection')
    return min(xs) if side=='left' else max(xs)

def place_panel(scene,camera,image,frame,anchor,side,gap_fraction,width=3.5,edge_u=None):
    """Align framed lower inner corner to anchor height, with horizontal screen gap.

    gap_fraction is a fraction of image width (gap_mm / publication_width_mm).
    Call again after moving a camera, instrument, or changing the frame size.
    """
    aspect=next(n.image.size[1]/n.image.size[0] for n in image.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE')
    fw,fh=width+.16,width*aspect+.16
    q=camera.matrix_world.to_quaternion();right=q@Vector((1,0,0));up=q@Vector((0,1,0));normal=q@Vector((0,0,1))
    p=project(scene,camera,anchor);depth=-(camera.matrix_world.inverted()@anchor).z
    sign=-1 if side=='left' else 1
    edge=p.x if edge_u is None else edge_u
    inner=unproject(scene,camera,(edge+sign*gap_fraction,p.y),depth)
    center=inner+right*(sign*fw/2)+up*(fh/2)
    frame.rotation_euler=camera.rotation_euler;frame.location=center-normal*.08;frame.dimensions=(fw,fh,.16)
    image.rotation_euler=camera.rotation_euler;image.location=center+normal*.02;image.scale=(width/3.5,width*aspect/3.5,1)
    frame.visible_shadow=False;image.visible_shadow=False
    actual=project(scene,camera,center-right*(sign*fw/2)-up*(fh/2))
    assert abs(actual.y-p.y)<1e-5
    assert abs(abs(actual.x-edge)-gap_fraction)<1e-5
    assert (q@Vector((0,0,1))).dot(image.rotation_euler.to_matrix()@Vector((0,0,1)))>.99999
    return {'image':image.name,'instrument_anchor_world':list(anchor),'panel_inner_lower_corner_world':list(inner),'gap_fraction':gap_fraction,'instrument_silhouette_edge_u':edge,'visible_horizontal_gap_pixels':abs(actual.x-edge)*scene.render.resolution_x,'gap_mm_at_86mm':gap_fraction*86,'vertical_error_pixels':abs(actual.y-p.y)*scene.render.resolution_y,'alignment':'panel lower-right to rear lower-left' if side=='left' else 'panel lower-left to front lower-right','camera_parallel':True}
