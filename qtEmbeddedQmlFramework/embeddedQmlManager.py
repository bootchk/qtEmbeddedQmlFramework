
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import qmlRegisterType

from qtEmbeddedQmlFramework.embeddedQmlInterface import EmbeddedQmlInterface
from qtEmbeddedQmlFramework.qmlFinder import QmlFinder
from qtEmbeddedQmlFramework.resourceManager import resourceMgr
from qtEmbeddedQmlFramework.windowManager import windowMgr

'''
Running with Python as top: use pyrcc5 to compile resources into <app>_rc.py.
Running pyqtdeploy'ed with C top calling embedded Python: use rcc to compile resources into a .cpp file,
the same one that pyqtdeploy reads frozen code from.
'''


class EmbeddedQmlManager(object):
  '''
  Knows how to set up bidirectional interface: embedded QML to app.
  
  For each top level embedded QML component in interfaces list:
  - create QQuickView 
  - find corresponding model delegate instance (optional)
  - find corresponding model context menu instance (optional)
  
  After instantiating and using, self is NOT garbage collected.
  References to all object instances created by self are kept in delegates OR self.quickViews.
  '''
  
  def __init__(self, subsystemName=None):
    " Keep reference so QQuickViews not garbage collected.  But app usually does not reference it. "
    self.quickViews = []
    self.subsystemName = subsystemName  # name of subdirectory of .../resources/qml
    
  
  def registerTypeInQml(self, typeToRegister):
    '''
    Register a type in QML.
    
    Simplified:
    -Use type's name as both the QML module name and the ???
    -Always use 1.0 as the QML version.
    '''
    #assert isinstance(typeToRegister, type), "connectionType is a Python Type"
    #qmlRegisterType(typeToRegister, 'Delegates', 1, 0, 'DocumentDelegate')
    print("Registering: ", typeToRegister.__name__)
    qmlRegisterType(typeToRegister, typeToRegister.__name__, 1, 0, typeToRegister.__name__)
    
  
  def createInterfaces(self, delegates, interfaces):
    '''
    Register types and create quickviews for interfaces, remembering delegates in delegates dictionary.
    
    If the QML for the interfaces uses other types, register them firts.
    '''
    
    " Supporting machinery common to each "
    qmlFinder = QmlFinder() 
    
    if self.subsystemName is None:
      # Usually caller is the main app
      subpath = 'views/'  # !!! all interfaces must be in .../qml/views/ directory
    else:
      # Usually caller is a subsystem
      subpath = self.subsystemName + '/views/' # e.g. print/views
    
    for interface in interfaces:
      assert isinstance(interface, EmbeddedQmlInterface)
      
      " Register a model delegate type defined by the widget app. "
      self.registerTypeInQml(typeToRegister = interface.delegateType)
      
      quickView = self._createQuickViewInstance(subpath, delegates, interface)
      " assert quickview has instantiated model of the registered type "
      self._keepReference(quickView)
      
      " Find model delegate instance so can connect app signals to QML to enable QML Actions"
      if interface.modelDelegateName is not None:
        delegates[interface.modelDelegateName] = qmlFinder.findDelegate(quickView, interface.delegateType, interface.name + "Delegate")
   
      " need context menu delegates so we can invoke them "
      if interface.modelContextMenuName is not None:
        delegates[interface.modelContextMenuName] = qmlFinder.findQMLComponentByName(quickView, interface.name + "ContextMenu")
    
    print("Done initting embedded qml")
    # all delegates of proper type
    
    
  def _createQuickViewInstance(self, subpath, delegates, interface):
    '''
    This is separate method because I experienced failures using the QQuickView(QUrl) signature:
    quietly hangs when root of qml is not descended from QQuickItem.
    Root cannot be Dialog{}; instead nest Item{ Dialog{}}
    
    Better to use the QQuickView() signature and then call setSource()
    Set env var QML_IMPORT_TRACE=1 to debug QML imports
    '''
    print("Creating quickView")
    quickView = QQuickView()
    
    
    # TEMP HACK
    # set transientParent to the app's root window.
    quickView.setTransientParent(windowMgr.getRootWindow())
    
    '''
    qurl = self._qmlFilenameToQUrl(subpath + interface.qmlFilename)
    '''
    qurl = resourceMgr.urlToQMLResource(resourceSubpath=subpath + interface.qmlFilename)
    print("Reading qml from:", qurl.path())
    quickView.setSource(qurl)
    return quickView



  def _keepReference(self, quickView):
    " Keep reference so not garbage collected."
    self.quickViews.append(quickView)
    
    # Alternative: stuff it in delegates dict
    #print(interface.name + 'S')
    #delegates[interface.name + 'S']=quickView
    
  

