import logging
logger = logging.getLogger("morse." + __name__ )
import morse.core.robot

class Arm( morse.core.robot.Robot ):

  def __init__( self, obj, parent=None ):

    logger.info( '%s initialization' % obj.name )
    super( self.__class__, self ).__init__( obj, parent )

    logger.info( 'component initialized' )

  def default_action( self ):
    """ Main function of this component """
    pass
