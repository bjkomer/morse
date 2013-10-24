import logging; logger = logging.getLogger("morse." + __name__)
import json
from morse.middleware.socket_datastream import SocketPublisher

class DVSCameraPublisher(SocketPublisher):

    _type_name = "a JSON-encoded image"

    def encode(self):
        res = {}
        res['height'] = self.component_instance.image_height
        res['width'] = self.component_instance.image_width
        res['image'] = self.component_instance.local_data['image'].tolist()
        
        return ( json.dumps( res ) + '\n' ).encode()
