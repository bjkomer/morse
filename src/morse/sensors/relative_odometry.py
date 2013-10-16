# <path>/morse/sensors/odometry.py

import logging; logger = logging.getLogger("morse." + __name__)
from morse.helpers.morse_math import normalise_angle
import morse.core.sensor
import copy
from morse.helpers.components import add_data, add_level, add_property

class RelativeOdometry(morse.core.sensor.Sensor):

    _name = "RelativeOdometry"
    _short_desc = "An odometry sensor that returns relative displacement information between two components."
    
    add_data('x', 0.0, "float","X coordinate of the sensor")
    add_data('y', 0.0, "float","Y coordinate of the sensor")
    add_data('z', 0.0, "float","Z coordinate of the sensor")
    add_data('yaw', 0.0, "float","rotation angle with respect to the Z axis")
    add_data('pitch', 0.0, "float","rotation angle with respect to the Y axis")
    add_data('roll', 0.0, "float","rotation angle with respect to the X axis")
    add_data('vx', 0.0, "float","linear velocity related to the X coordinate of the sensor")
    add_data('vy', 0.0, "float","linear velocity related to the Y coordinate of the sensor")
    add_data('vz', 0.0, "float","linear velocity related to the Z coordinate of the sensor")
    add_data('wz', 0.0, "float","angular velocity related to the Z coordinate of the sensor")
    add_data('wy', 0.0, "float","angular velocity related to the Y coordinate of the sensor")
    add_data('wx', 0.0, "float","angular velocity related to the X coordinate of the sensor")
    
    add_property('_from_comp', "", 'from_component', 'string',
                 'name of the component that measurements are made starting from')
    add_property('_to_comp', "", 'to_component', 'string',
                 'name of the component that measurements are made towards')

    def __init__(self, obj, parent=None):
        # Call the constructor of the parent class
        super(RelativeOdometry, self).__init__(obj, parent)
        
        self.original_pos = copy.copy(self.position_3d)

        self.previous_pos = self.original_pos.transformation3d_with(
                                                            self.position_3d)

        logger.info('Component initialized')
    
    def default_action(self):
        # Compute the position of the base within the original frame
        #current_pos = self.original_pos.transformation3d_with(self.position_3d)
        # Compute the position of the sensor relative to the base
        import bge
        to_obj = bge.logic.getCurrentScene().objects[ self._to_comp ]
        from_obj = bge.logic.getCurrentScene().objects[ self._from_comp ]
        
        from_ang = from_obj.worldOrientation.to_euler()
        to_ang = to_obj.worldOrientation.to_euler()
        
        from_ang_vel = from_obj.worldAngularVelocity
        to_ang_vel = to_obj.worldAngularVelocity
        
        from_pos = from_obj.worldPosition
        to_pos = to_obj.worldPosition

        from_lin_vel = from_obj.worldLinearVelocity
        to_lin_vel = to_obj.worldLinearVelocity

        # Integrated version
        self.local_data['x'] = to_pos.x - from_pos.x
        self.local_data['y'] = to_pos.y - from_pos.y
        self.local_data['z'] = to_pos.z - from_pos.z
        self.local_data['yaw'] = to_ang.z - from_ang.z #current_pos.yaw
        self.local_data['pitch'] = to_ang.y - from_ang.y #current_pos.pitch
        self.local_data['roll'] = to_ang.x - from_ang.x #current_pos.roll

        # TODO: make these accurate as well
        # speed in the sensor frame, related to the robot pose
        """
        self.delta_pos = self.previous_pos.transformation3d_with(current_pos)
        self.local_data['vx'] = self.delta_pos.x * self.frequency
        self.local_data['vy'] = self.delta_pos.y * self.frequency
        self.local_data['vz'] = self.delta_pos.z * self.frequency
        self.local_data['wz'] = self.delta_pos.yaw * self.frequency
        self.local_data['wy'] = self.delta_pos.pitch * self.frequency
        self.local_data['wx'] = self.delta_pos.roll * self.frequency
        """
        self.local_data['vx'] = to_lin_vel.x - from_lin_vel.x
        self.local_data['vy'] = to_lin_vel.y - from_lin_vel.y
        self.local_data['vz'] = to_lin_vel.z - from_lin_vel.z
        self.local_data['wz'] = to_ang_vel.x - from_ang_vel.x
        self.local_data['wy'] = to_ang_vel.y - from_ang_vel.y
        self.local_data['wx'] = to_ang_vel.z - from_ang_vel.z


        # Store the 'new' previous data
        self.previous_pos = current_pos
