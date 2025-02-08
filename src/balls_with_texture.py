import bpy
import bmesh
import mathutils

# ----------------------------
# MATERIAL & PARTICLE SETUP
# ----------------------------

def create_particle_object():
    """Create instanced particle geometry"""
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.05)
    particle_obj = bpy.context.active_object
    particle_obj.name = "ParticleInstance"
    
    mat = bpy.data.materials.new(name="ParticleGlow")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    principled.inputs['Emission Strength'].default_value = 5.0
    principled.inputs['Emission Color'].default_value = (0.8, 0.2, 0.8, 1)
    
    particle_obj.data.materials.append(mat)
    return particle_obj

def create_entangled_material(name):
    """Create material with Stability AI integration"""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    # Stability AI Node Setup
    sd_node = nodes.new(type='CompositorNodeStableDiffusion')
    sd_node.location = (-800, 0)
    sd_node.prompt = "swirling quantum particles, energy threads, neon glow trails, motion blur, 8k scifi"
    sd_node.negative_prompt = "static, smooth, solid colors, perfect symmetry"
    sd_node.steps = 35
    sd_node.cfg_scale = 11
    sd_node.sampler = 'DPM++ 2M Karras'
    sd_node.inputs['Init Strength'].default_value = 0.45

    # Material Output Setup
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    principled.location = (-400, 0)
    output.location = (0, 0)
    
    # Node Connections
    links = mat.node_tree.links
    links.new(sd_node.outputs[0], principled.inputs['Emission'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    # Animated Noise Driver
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-1200, 0)
    noise.inputs['Scale'].default_value = 5.0
    links.new(noise.outputs['Fac'], sd_node.inputs['Noise Influence'])
    
    # Animate noise scale
    noise.inputs['Scale'].keyframe_insert('default_value', frame=1)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Scale'].keyframe_insert('default_value', frame=250)
    
    return mat

# ----------------------------
# GEOMETRY CREATION
# ----------------------------

def create_quantum_ball(location):
    """Create sphere with particle system"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=location)
    ball = bpy.context.active_object
    
    # Assign entangled material
    if "QuantumMaterial" not in bpy.data.materials:
        mat = create_entangled_material("QuantumMaterial")
    else:
        mat = bpy.data.materials["QuantumMaterial"]
    
    ball.data.materials.clear()
    ball.data.materials.append(mat)

    # Add particle system
    ball.modifiers.new(name="Particles", type='PARTICLE_SYSTEM')
    psys = ball.particle_systems[-1].settings
    psys.count = 300
    psys.frame_start = 1
    psys.frame_end = 1
    psys.lifetime = 250
    psys.emit_from = 'VOLUME'
    psys.physics_type = 'NEWTON'
    psys.render_type = 'OBJECT'
    psys.instance_object = bpy.data.objects.get("ParticleInstance")

    return ball

def create_energy_edge(start, end):
    """Create glowing connection between points"""
    mesh = bpy.data.meshes.new("EnergyEdge")
    obj = bpy.data.objects.new("EnergyEdge", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    v1 = bm.verts.new(start)
    v2 = bm.verts.new(end)
    bm.edges.new((v1, v2))
    bm.to_mesh(mesh)
    bm.free()
    
    # Add material
    if "EnergyMaterial" not in bpy.data.materials:
        mat = create_entangled_material("EnergyMaterial")
    else:
        mat = bpy.data.materials["EnergyMaterial"]
    
    obj.data.materials.append(mat)
    
    # Add curve modifier
    obj.modifiers.new(name="Wave", type='CURVE')
    return obj

# ----------------------------
# SCENE SETUP
# ----------------------------

def setup_scene():
    """Configure scene settings"""
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    bpy.context.scene.eevee.taa_render_samples = 64
    bpy.context.scene.frame_end = 250
    
    # Add subtle volumetric lighting
    bpy.context.scene.world.use_nodes = True
    nodes = bpy.context.scene.world.node_tree.nodes
    nodes.new(type='ShaderNodeVolumePrincipled')
    nodes.new(type='ShaderNodeVolumeAbsorption')
    output = nodes.get('World Output')
    
    links = bpy.context.scene.world.node_tree.links
    links.new(nodes['Principled Volume'].outputs[0], output.inputs['Volume'])

# ----------------------------
# MAIN EXECUTION
# ----------------------------

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create core elements
create_particle_object()
positions = [
    (0, 0, 0),
    (3, 0, 0),
    (0, 3, 0),
    (0, 0, 3)
]

balls = [create_quantum_ball(pos) for pos in positions]

# Create entanglement connections
create_energy_edge(positions[0], positions[1])
create_energy_edge(positions[1], positions[2])
create_energy_edge(positions[2], positions[3])
create_energy_edge(positions[3], positions[0])
create_energy_edge(positions[0], positions[2])
create_energy_edge(positions[1], positions[3])

# Final scene setup
setup_scene()
bpy.ops.object.select_all(action='DESELECT')

def ensure_camera():
    cam = None
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            cam = obj
            break
    if not cam:
        bpy.ops.object.camera_add(location=(0, -10, 5), rotation=(1.1, 0, 0))
        cam = bpy.context.active_object
    bpy.context.scene.camera = cam

ensure_camera()

print("Quantum entanglement system created! Press F12 to render.")
