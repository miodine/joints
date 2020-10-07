import vpython as vp
import keyboard as k
#import numpy as np

import joints

## state/space variables
# world baseframe
x0 = 0
y0 = 0
z0 = 0

dt = 0.033      # time quantum abstraction
v = 5           # linear velocity abstraction

## background configuration
scene = vp.canvas()
scene.background = vp.vector(135/255, 206/255, 250/255)
base = vp.box(pos=vp.vector(x0, y0, z0), length=40, height=0.1, width=40)
base.texture = vp.textures.metal


## Initialise kinematic chain with reference to some base vpython object

kinch = joints.kinematic_chain(base)

## Appending joints to the kinematic chain 

kinch.add(type_ = 'trans', axis_of_operation = 'x', m_stroke= 10)
kinch.add(type_ = 'trans', axis_of_operation = 'y', m_stroke= 10)
kinch.add(type_ = 'trans', axis_of_operation = 'z', m_stroke= 10)
kinch.add(type_ = 'rot', axis_of_operation = 'y', ifr_dist= 0)
kinch.add(type_ = 'rig', axis_of_operation = '-x', ifr_dist= 10)
kinch.add(type_ = 'rot', axis_of_operation = 'z', ifr_dist= 0)
kinch.add(type_ = 'trans', axis_of_operation = 'x', m_stroke= 10)

# types of joints (as for now): 'rig' -rigid, 'trans' - translational,
#                               'rot' - rotational 
#
# axis_of_operation defines orientation of secondary joint component, w.r.t. 
# the primary joint component. 'x' defines direction that parallel the 'x' axis
# in the "base coordinate frame". '-x' works the same way, but the orientation 
# will be oposite. ie. 'x' = 1i, '-x' = -1i (i = unit vector along x axis)
# 
# m_stroke -> maximal stroke parameter, only for translational joints ('dynamic')
# ifr_dist -> distance between first and second frames (two cyllinders, two boxes) 
#             constituting a joint; only for rotational and rigid joints ('static')






## snippet of code for controlling the joints
# legend: num keys ==>> selecting the joint of a kinematic chain to control 
#         +/-      ==>> extruding/rotating (type dependent) joint at a rate of v, or -v

toggle = 0

while(True):
    vp.rate(pow(dt, -1))
    for i in range(kinch.get_length()):
        kinch.set_colour(i, vp.vector(1,1,1))
        if k.is_pressed(str(i)):
            toggle = i
    kinch.set_colour(toggle, vp.vector(254/255, 216/255, 177/255))
    if k.is_pressed('+'):
        kinch.control(joint_id_ = toggle, op_amount_= v*dt)
    elif k.is_pressed('-'):
        kinch.control(joint_id_ = toggle, op_amount_= -v*dt)


    # UPDATE
