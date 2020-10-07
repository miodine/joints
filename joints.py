import vpython as vp
import numpy as np

#DEFAULT COMPONENT SIZE
DCS_ =  10 

class translational_joint():
    __max_stroke = DCS_*2
    __min_stroke = DCS_

    def __init__(self, trans_axis, position, max_stroke = None):
        self.__max_stroke = self.__min_stroke + max_stroke
        self.__translation_axis = trans_axis
        #CONVENTION_MARKER_SIZE
        self.begin_box = vp.box(pos= position, length= DCS_, height= DCS_, width= DCS_)
        self.joint_box = vp.box(pos=self.begin_box.pos, length=DCS_*0.5, height=DCS_*0.5, width=DCS_*0.5, opacity=0.8)
        self.joint_box.color = vp.vector(1, 0, 0)


        self.end_box = vp.box(pos=self.begin_box.pos, length= DCS_, height= DCS_, width= DCS_)
        if self.__translation_axis == 'x':
            self.end_box.pos.x += self.begin_box.length

        elif self.__translation_axis == 'y':
            self.end_box.pos.y += self.begin_box.width
        
        elif self.__translation_axis == 'z':
           self.end_box.pos.z += self.begin_box.height

        elif self.__translation_axis == '-x':
            self.end_box.pos.x -= self.begin_box.length
        
        elif self.__translation_axis == '-y':
            self.end_box.pos.y -= self.begin_box.length

        elif self.__translation_axis == '-z':
            self.end_box.pos.z -= self.begin_box.length


        else:
            print("Undefined: translation axis undefined")
            exit(69)
        
       

        self.position = self.end_box.pos

    def update_joint(self):
        self.joint_box.pos = (self.begin_box.pos + self.end_box.pos)
        self.joint_box.pos.x *= 0.5
        self.joint_box.pos.y *= 0.5
        self.joint_box.pos.z *= 0.5

        if self.__translation_axis == 'x' or self.__translation_axis == '-x':
            self.joint_box.length = vp.mag(self.end_box.pos-self.begin_box.pos)
        elif self.__translation_axis == 'y' or self.__translation_axis == '-y':
            self.joint_box.height = vp.mag(self.end_box.pos - self.begin_box.pos)
        elif self.__translation_axis == 'z' or self.__translation_axis == '-z':
            self.joint_box.width = vp.mag(self.end_box.pos - self.begin_box.pos)

    ##rotation overload 
    def rotate(self, angle, axis, origin):
        #change the global orientation of the structure
        self.begin_box.rotate(angle, axis = axis, origin = origin)
        self.joint_box.rotate(angle, axis = axis, origin = origin)
        self.end_box.rotate(angle, axis = axis, origin = origin)
        self.position = self.end_box.pos


    def translate(self, translation: vp.vector):
        #change the global coordinates of the structure's origin
        #translation -> vector(translation_velocity) * dt
        self.begin_box.pos += translation
        self.joint_box.pos += translation
        self.end_box.pos += translation
        self.position = self.end_box.pos
    

    def __extrude_assign(self, stroke, direction):
        #helper function to extrude()
        self.end_box.pos.x += direction.x*stroke
        self.end_box.pos.y += direction.y*stroke
        self.end_box.pos.z += direction.z*stroke

    def extrude(self, stroke):
        #EXTRUDE THE SHAAAFTT 
        #stroke => stroke_velocity*dt
        mag = vp.mag(self.end_box.pos - self.begin_box.pos)
        direction = vp.hat(self.end_box.pos - self.begin_box.pos)
        if mag <= self.__max_stroke and mag >=self.__min_stroke:        
            self.__extrude_assign(stroke, direction)
            return direction

        #update blocking
        if mag > self.__max_stroke:
            if stroke > 0:
                return vp.vector(0,0,0)
            else:
                self.__extrude_assign(stroke, direction)
                return direction
        elif mag < self.__min_stroke:
            if stroke < 0:
                return vp.vector(0,0,0)
            else: 
                self.__extrude_assign(stroke, direction)
                return direction



    def get_type(self):
        return ['trans', self.__translation_axis]

    def get_axis(self):
        return self.end_box.pos - self.begin_box.pos
    
    def get_position(self):
        return self.end_box.pos 
    
    def update_position(self, position):
        pass
    
    def set_colour(self, colour: vp.vector):
        self.begin_box.color = colour
        self.end_box.color = colour

class rotational_joint():

    def __init__(self, rot_axis: str, position: vp.vector, i_frame_distance: int):

        self.__rotation_axis = rot_axis
        if self.__rotation_axis == 'x':
            self.begin_cylinder = vp.cylinder(pos = position, axis = vp.vector(DCS_,0,0), radius = DCS_/2)
            self.end_cylinder = vp.cylinder(pos = position + vp.vector(i_frame_distance+DCS_,0,0) , axis = vp.vector(DCS_,0,0), radius = DCS_/2)
            self.joint_cylinder = vp.cylinder(pos = self.begin_cylinder.pos + vp.vector(DCS_,0,0), axis = vp.vector(i_frame_distance,0,0), radius = DCS_/4, opacity = 0.75 )


        elif self.__rotation_axis == '-x':
            self.begin_cylinder = vp.cylinder(pos = position, axis = vp.vector(-DCS_,0,0), radius = DCS_/2)
            self.end_cylinder = vp.cylinder(pos = position - vp.vector(i_frame_distance+DCS_,0,0) , axis = vp.vector(-DCS_,0,0), radius = DCS_/2)
            self.joint_cylinder = vp.cylinder(pos = self.begin_cylinder.pos - vp.vector(DCS_,0,0), axis = vp.vector(-i_frame_distance,0,0), radius = DCS_/4, opacity = 0.75 )
        
        
        elif self.__rotation_axis == 'y':
            self.begin_cylinder = vp.cylinder(pos = position, axis = vp.vector(0,DCS_,0), radius = DCS_/2)
            self.end_cylinder = vp.cylinder(pos = position + vp.vector(0,i_frame_distance+DCS_,0) , axis = vp.vector(0,DCS_,0), radius = DCS_/2)
            self.joint_cylinder = vp.cylinder(pos = self.begin_cylinder.pos + vp.vector(0,DCS_,0), axis = vp.vector(0,i_frame_distance,0), radius = DCS_/4, opacity = 0.75 )

        elif self.__rotation_axis == '-y':
            self.begin_cylinder = vp.cylinder(pos = position, axis = vp.vector(0,-DCS_,0), radius = DCS_/2)
            self.end_cylinder = vp.cylinder(pos = position - vp.vector(0,i_frame_distance+DCS_,0) , axis = vp.vector(0,DCS_,0), radius = DCS_/2)
            self.joint_cylinder = vp.cylinder(pos = self.begin_cylinder.pos - vp.vector(0,DCS_,0), axis = vp.vector(0,-i_frame_distance,0), radius = DCS_/4, opacity = 0.75 )

        
        elif self.__rotation_axis == 'z':
            self.begin_cylinder = vp.cylinder(pos = position, axis = vp.vector(0,0,DCS_), radius = DCS_/2)
            self.end_cylinder = vp.cylinder(pos = position + vp.vector(0,0,i_frame_distance+DCS_) , axis = vp.vector(0,0,DCS_), radius = DCS_/2)
            self.joint_cylinder = vp.cylinder(pos = self.begin_cylinder.pos + vp.vector(0,0,DCS_), axis = vp.vector(0,0,i_frame_distance), radius = DCS_/4, opacity = 0.75 )
        
        elif self.__rotation_axis == '-z':
            self.begin_cylinder = vp.cylinder(pos = position, axis = vp.vector(0,0,-DCS_), radius = DCS_/2)
            self.end_cylinder = vp.cylinder(pos = position - vp.vector(0,0,i_frame_distance+DCS_) , axis = vp.vector(0,0,DCS_), radius = DCS_/2)
            self.joint_cylinder = vp.cylinder(pos = self.begin_cylinder.pos - vp.vector(0,0,DCS_), axis = vp.vector(0,0,-i_frame_distance), radius = DCS_/4, opacity = 0.75 )

        
        else:
            print("Error on creation: ")
        
        self.joint_cylinder.color = vp.vector(0,0,1)
        self.position = self.end_cylinder.pos

    def rotate(self, angle, axis, origin):
        #change the global orientation of the structure
        self.begin_cylinder.rotate(angle, axis = axis, origin = origin)
        self.joint_cylinder.rotate(angle, axis = axis, origin = origin)
        self.end_cylinder.rotate(angle, axis = axis, origin = origin)
    
    def translate(self, translation: vp.vector):
        #change the global coordinates of the structure's origin
        #translation -> vector(translation_velocity) * dt
        self.begin_cylinder.pos += translation
        self.joint_cylinder.pos += translation
        self.end_cylinder.pos += translation
    
    def get_type(self):
        return ['rot', self.__rotation_axis]
    
    def get_position(self):
        return self.end_cylinder.pos 

    def get_axis(self):
        if (self.end_cylinder.pos - self.begin_cylinder.pos) == vp.vector(0,0,0):
            if self.__rotation_axis == 'x' or self.__rotation_axis == '-x':
                return vp.vector(1,0,0)
            elif self.__rotation_axis == 'y' or self.__rotation_axis == '-y':
                return vp.vector(0,1,0)
            elif self.__rotation_axis == 'z' or self.__rotation_axis == '-z':
                return vp.vector(0,0,1)
        
        return self.end_cylinder.pos - self.begin_cylinder.pos
    
    def update_joint(self):
        pass


    #DO WYJEBANIA vvv MONGOLSTWO XD
    def set_colour(self, colour: vp.vector ):

        self.begin_cylinder.color = colour
        self.end_cylinder.color = colour

class rigid_joint(translational_joint):

    #constructor overload
    def __init__(self, axis: str, position: vp.vector, i_fr_distance: int ,end_pos = None):

        self.__axis = axis
        #CONVENTION_MARKER_SIZE
        self.begin_box = vp.box(pos= position, length= DCS_, height= DCS_, width= DCS_)
        self.joint_box = vp.box(pos=self.begin_box.pos, length=DCS_*0.5, height=DCS_*0.5, width=DCS_*0.5, opacity=0.8)
        self.joint_box.color = vp.vector(0, 0, 1)
        
        self.end_box = vp.box(pos=self.begin_box.pos , length= DCS_, height= DCS_, width= DCS_)

        if self.__axis == 'x':
            self.end_box.pos.x += i_fr_distance
            #self.joint_box.length += i_fr_distance
        elif self.__axis == '-x':
            self.end_box.pos.x -= i_fr_distance


        elif self.__axis == 'y':
            self.end_box.pos.y +=  i_fr_distance
        
        elif self.__axis == '-y':
            self.end_box.pos.y -=  i_fr_distance

        elif self.__axis == 'z':
           self.end_box.pos.z += i_fr_distance

        elif self.__axis == '-z':
           self.end_box.pos.z -= i_fr_distance
        else:
            print("a teraz pyton spenetruje ci dupsko: err 69")
            exit(69)

        self.position = self.end_box.pos
        self.update_joint()

    def extrude(self, stroke):
        pass

    def get_type(self):
        return ['rigid', self.__axis]
    
    def update_joint(self):
        self.joint_box.pos = (self.begin_box.pos + self.end_box.pos)
        self.joint_box.pos.x *= 0.5
        self.joint_box.pos.y *= 0.5
        self.joint_box.pos.z *= 0.5

        if self.__axis == 'x' or self.__axis == '-x':
            self.joint_box.length = vp.mag(self.end_box.pos-self.begin_box.pos)

        elif self.__axis == 'y' or self.__axis == '-y':
            self.joint_box.height = vp.mag(self.end_box.pos - self.begin_box.pos)

        elif self.__axis == 'z' or self.__axis == '-z':
            self.joint_box.width = vp.mag(self.end_box.pos - self.begin_box.pos)

class kinematic_chain():
    __chain = []
    def __init__(self, base):
        self.__chain.append(base)

    def __rotational_assignment(self, DCS_mod, type_):
        if type_ == 'x':
            add_pos = vp.vector(DCS_*DCS_mod,0,0)

        elif type_ == '-x':
            add_pos = vp.vector(-DCS_*DCS_mod,0,0)

        elif type_ == 'y':
            add_pos = vp.vector(0,DCS_*DCS_mod,0)
                    
        elif type_ == '-y':
            add_pos = vp.vector(0,-DCS_*DCS_mod,0)

        elif type_ == 'z':
            add_pos = vp.vector(0,0, DCS_*DCS_mod)
                    
        elif type_ == '-z':
            add_pos = vp.vector(0,0, -DCS_*DCS_mod)        

        return add_pos


    def add(self, type_: str, axis_of_operation: str, m_stroke = None, ifr_dist = None):
        first_ = False
        #determine if added joint is base or not (ie first in the list)
        if len(self.__chain) == 1:
           first_ = True
        else: 
            first_ = False
        #append joint

        if type_ == ('trans' or 'translational'):
            if first_:
                to_app = translational_joint(axis_of_operation, self.__chain[0].pos + vp.vector(0,DCS_,0), m_stroke)
                self.__chain.append(to_app)
            else:
                add_pos = vp.vector(0,0,0)
                prev_type = self.__chain[len(self.__chain)-1].get_type()
                prev_pos = self.__chain[len(self.__chain)-1].get_position()

                if prev_type[0] == 'rot':
                    add_pos = self.__rotational_assignment(1,prev_type[1])

                to_app = translational_joint(axis_of_operation, prev_pos + add_pos, m_stroke) 
                self.__chain.append(to_app)

        if type_ == ('rot' or 'rotational'):
            if first_:
                to_app = rotational_joint(rot_axis = axis_of_operation, position = self.__chain[0].pos + vp.vector(0,DCS_,0), i_frame_distance = ifr_dist)
                self.__chain.append(to_app)
            else:
                add_pos = vp.vector(0,0,0)
                prev_type = self.__chain[len(self.__chain)-1].get_type()
                prev_pos = self.__chain[len(self.__chain)-1].get_position()
                
                
                if prev_type[0] == 'rot':
                    add_pos = self.__rotational_assignment(0.5,prev_type[1])

                to_app = rotational_joint(axis_of_operation, prev_pos + add_pos, ifr_dist) 
                self.__chain.append(to_app)

                
        if type_ == ('rig' or 'rigid'):

            if first_:
                to_app = rigid_joint(axis_of_operation, self.__chain[0].pos + vp.vector(0,DCS_,0), ifr_dist)
                self.__chain.append(to_app)
            else:
                add_pos = vp.vector(0,0,0)
                prev_type = self.__chain[len(self.__chain)-1].get_type()
                prev_pos = self.__chain[len(self.__chain)-1].get_position()
                
                if prev_type[0] == 'rot':
                    add_pos = self.__rotational_assignment(1,prev_type[1])

                to_app = rigid_joint(axis_of_operation, prev_pos + add_pos, ifr_dist) 
                self.__chain.append(to_app)


    def get_length(self):
        return len(self.__chain)
    

    #DO WYJEBANIA vvv TRZEBA TO MĄDRZEJ ZROBIĆ
    def set_colour(self,id_: int, colour_: vp.vector):
        if id_ == 0:
            pass
        else:
            self.__chain[id_].set_colour(colour_)


    def control(self, joint_id_: int, op_amount_: float):
        #op_amount = v*dt for translation
        #op_amount = omega*dt for rotation
        if joint_id_ == 0:
            pass
        else: 
            type_ = self.__chain[joint_id_].get_type()
            if type_[0] == ('trans'):
                dir_vec = self.__chain[joint_id_].extrude(op_amount_)
                self.__chain[joint_id_].update_joint()
                for i in range(joint_id_+1, len(self.__chain)):
                    self.__chain[i].translate(dir_vec*op_amount_)

            elif type_[0] == 'rot':
                origin = self.__chain[joint_id_].get_position()
                axis = self.__chain[joint_id_].get_axis()
                
                for i in range(joint_id_+1, len(self.__chain)):
                    self.__chain[i].rotate(op_amount_, axis, origin)
            #elif type == rigid: pass ???