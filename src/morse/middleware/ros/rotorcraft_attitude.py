import roslib; roslib.load_manifest('geometry_msgs')
from geometry_msgs.msg import Quaternion # FIXME: temporarily using this for now
from morse.middleware.ros import ROSSubscriber


class AttitudeReader(ROSSubscriber):
    """ Subscribe to a rotorcraft attitude command and set 
        the fields of the quaternion to be roll, pitch, yaw, and thrust. """
    ros_class = Quaternion

    # TODO: put the right stuff here
    def update(self, message):
        self.data["roll"] = message.x
        self.data["pitch"] = message.y
        self.data["yaw"] = message.z
        self.data["thrust"] = message.w
