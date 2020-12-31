import bpy
from math import radians
import random
import mathutils

random.seed(a=None, version=2)

tx = 0.0
ty = 0.0
tz = 30

rx = 0.0
ry = 0.0
rz = 0.0

fov = 30

pi = 3.14159265

scene = bpy.data.scenes["Scene"]

# Set render resolution
scene.render.resolution_x = 500
scene.render.resolution_y = 500

# Set camera fov in degrees
scene.camera.data.angle = fov*(pi/180.0)

## Set camera rotation in euler angles
#scene.camera.rotation_mode = 'XYZ'
#scene.camera.rotation_euler[0] = rx*(pi/180.0)
#scene.camera.rotation_euler[1] = ry*(pi/180.0)
#scene.camera.rotation_euler[2] = rz*(pi/180.0)

# Set camera translation
scene.camera.location.x = tx
scene.camera.location.y = ty
scene.camera.location.z = tz

  
def random_rotate_render_and_write(output_dir, output_render_pattern_string = 'render%d.jpg', output_text_pattern_string = 'label%d.txt', iter_max = 200, dmin = 15, dmax = 50, subject = bpy.data.objects, sun = bpy.data.objects):
  import os
  original_rotation = scene.camera.rotation_euler
  for iter in range(0, iter_max):
    #set cam distance  
    scene.camera.location.z = random.uniform(dmin, dmax)
    
    #Set random rotation of the object
    subject.rotation_euler[0] = random.uniform(0, 360)*(pi/180.0)
    subject.rotation_euler[1] = random.uniform(0, 360)*(pi/180.0)
    subject.rotation_euler[2] = random.uniform(0, 360)*(pi/180.0)
    
    #Set random rotation of the sun
    sun.rotation_euler[0] = random.uniform(0, 360)*(pi/180.0)
    sun.rotation_euler[1] = random.uniform(0, 360)*(pi/180.0)
    sun.rotation_euler[2] = random.uniform(0, 360)*(pi/180.0)
    
    print('rendering image'+str(iter))
    bpy.context.scene.render.filepath = os.path.join(output_dir, (output_render_pattern_string % iter))
    bpy.ops.render.render(write_still = True)
    
    print('writing label'+str(iter))
    f= open(os.path.join(output_dir, (output_text_pattern_string % iter)) ,"w+")
    f.writelines('data_name : render%d.jpg\n')
    f.writelines('distance_cam : '+str(scene.camera.location.z)+'\n')
    f.writelines('rot_x : '+str(subject.rotation_euler[0])+'\n')
    f.writelines('rot_x : '+str(subject.rotation_euler[1])+'\n')
    f.writelines('rot_x : '+str(subject.rotation_euler[2])+'\n') 
    f.close() 
  

random_rotate_render_and_write('/Users/Kabilaan/Documents/SUPAERO_3A/Cours/PIE/Blender/render/snap_par_python', 'space_rider_render%d.jpg', 'space_rider_label%d.txt', iter_max = 5, dmin = 15, dmax = 100, subject = bpy.data.objects["space_rider"], sun = bpy.data.objects["Sun"])
