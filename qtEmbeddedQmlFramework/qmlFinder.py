
from PyQt5.QtCore import QObject


class QmlFinder(object):
  '''
  Find delegates, which are created on the QML side.
  Delegate types are registered on the Python side, but not instantiated.
  Find instances so that Python side can reference them.
  Find instances by searching tree of QObjects startig with the root of a QuickView that embeds QML.
  '''
  
  def findDelegate(self, quickView, delegateType, delegateObjectName):
    " by type and objectName"
    return self.findQMLComponents(quickView, delegateType, delegateObjectName)
    
  
  '''
  Workaround bug in findChild
  '''
  def findQMLComponents(self, quickView, aType, name):
    '''
    Find QML component by type and objectName.
    '''
    result = None
    children = quickView.rootObject().findChildren(QObject)
    for item in children:
      # Note the QML id property is NOT the objectName
      # print(item, item.objectName())
      if isinstance(item, aType) and item.objectName() == name:
        print("Found QML object", aType, name)
        result = item
        break
    assert result is not None
    return result
  
  def findQMLComponentByName(self, quickView, name):
    '''
    Find QML component by objectName.
    '''
    result = None
    children = quickView.rootObject().findChildren(QObject)
    for item in children:
      # Note the QML id property is NOT the objectName
      # print(item, item.objectName())
      if item.objectName() == name:
        print("Found QML object", name)
        result = item
        break
    assert result is not None
    return result