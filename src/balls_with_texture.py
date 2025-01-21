import bpy
import bmesh
import mathutils

def create_textured_material(material_name):
    # Create a material and enable nodes
    material = bpy.data.materials.new(material_name)
    material.use_nodes = True
    
    # Clear default nodes
    nodes = material.node_tree.nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create output node
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (500, 0)
    
    # Create Principled BSDF
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (200, 0)
    material.node_tree.links.new(principled.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Create a noise texture node
    noise_tex = nodes.new(type='ShaderNodeTexNoise')
    noise_tex.inputs["Scale"].default_value = 5.0
    noise_tex.location = (-400, 0)
    
    # Create a color ramp to adjust noise colors
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-150, 0)
    color_ramp.color_ramp.elements[0].color = (0.8, 0.2, 0.8, 1.0)  # Pinkish
    color_ramp.color_ramp.elements[1].color = (0.2, 0.6, 0.8, 1.0)  # Bluish
    
    # Link the nodes
    material.node_tree.links.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
    material.node_tree.links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    
    # Set the Emission color and strength to create a glow
    material.node_tree.links.new(color_ramp.outputs['Color'], principled.inputs['Emission'])
    principled.inputs['Emission Strength'].default_value = 2.0
    
    # Optional: Adjust metallic/roughness
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.4
    
    return material

def create_ball(location):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=location)
    ball = bpy.context.active_object
    
    if "EntangledBallMaterial" not in bpy.data.materials:
        ball_mat = create_textured_material("EntangledBallMaterial")
    else:
        ball_mat = bpy.data.materials["EntangledBallMaterial"]
    
    ball.data.materials.clear()
    ball.data.materials.append(ball_mat)

def create_edge(start, end):
    mesh = bpy.data.meshes.new(name="Edge")
    obj = bpy.data.objects.new(name="Edge", object_data=mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    v1 = bm.verts.new(start)
    v2 = bm.verts.new(end)
    bm.edges.new((v1, v2))
    bm.to_mesh(mesh)
    bm.free()
    
    if "EntangledEdgeMaterial" not in bpy.data.materials:
        edge_mat = create_textured_material("EntangledEdgeMaterial")
    else:
        edge_mat = bpy.data.materials["EntangledEdgeMaterial"]
    
    obj.data.materials.clear()
    obj.data.materials.append(edge_mat)

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create balls
ball1_location = (0, 0, 0)
ball2_location = (0, 0, 4)
ball3_location = (4, 0, 0)
ball4_location = (0, 4, 0)

create_ball(ball1_location)
create_ball(ball2_location)
create_ball(ball3_location)
create_ball(ball4_location)

# Create edges
create_edge(ball1_location, ball2_location)
create_edge(ball2_location, ball3_location)
create_edge(ball3_location, ball1_location)
create_edge(ball1_location, ball4_location)
create_edge(ball2_location, ball4_location)
create_edge(ball3_location, ball4_location)

print("3D object with 'entangled' glowing balls and edges created.")