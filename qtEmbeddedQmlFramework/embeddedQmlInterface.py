 
  
class EmbeddedQmlInterface(object):
  '''
  Simple data structure describing an interface to embedded QML.
  '''
  
  def __init__(self, delegateType, name, qmlFilename, modelDelegateName=None, modelContextMenuName=None):
    
    " Python type of a delegate "
    self.delegateType = delegateType
    
    " String name of interface. "
    self.name = name
    
    " file containing qml side of interface "
    self.qmlFilename = qmlFilename
    
    '''
    String key in dictionary of delegates.
    '''
    self.modelDelegateName = modelDelegateName
    
    '''
    String key in dictionary of delegates.
    If object is not a drawable, visible object (and has not context menu), pass None.
    '''
    self.modelContextMenuName = modelContextMenuName