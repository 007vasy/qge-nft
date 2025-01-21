import bpy
import mathutils

def create_ball(location):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=location)

def create_edge(start, end):
    mesh = bpy.data.meshes.new(name="Edge")
    obj = bpy.data.objects.new(name="Edge", object_data=mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.verts.new(start)
    bm.verts.new(end)
    bm.edges.new(bm.verts)
    bm.to_mesh(mesh)
    bm.free()

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create balls
ball1_location = (0, 0, 0)
ball2_location = (2, 2, 0)
ball3_location = (4, 0, 0)

create_ball(ball1_location)
create_ball(ball2_location)
create_ball(ball3_location)

# Create edges
create_edge(ball1_location, ball2_location)
create_edge(ball2_location, ball3_location)
create_edge(ball3_location, ball1_location)

print("3D object with 3 balls and edges created.")