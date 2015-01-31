
from PyQt5.QtCore import QFileInfo, QUrl



class ResourceManager(object):
  '''
  Knows how to find resources.
  
  When directories are structured as:
  
  app.py
  app/       package for app
     resources/
        qml/
           views/
              mainView.qml
           menus/
              aMenu.qml
        translations/
           app.qm
      package1   subpackage for app
           
  IOW resources directory is subdirectory of app's main package
  
  When you use pyqtdeploy, the entire package for app (including frozen modules, qml, and translations) is embedded in a .qrc file.
  '''
  
  def setResourceRoot(self, fileMainWasLoadedFrom, appPackageName):
    '''
    Set global to remember resource root.
    Assert self is part of app executable file (so __file__ is dir of app as deployed or running under Python.)
    
    Get name of the directory containing resources directory, 
    either a directory in the real filesystem,
    or in the in-memory filesystem created by rcc as called by pyqtdeploy.
    '''
    self._root = QFileInfo(fileMainWasLoadedFrom).absolutePath()
    print("Path to root: ", self._root)
    self._appPackageName = appPackageName
    
    
  def getResourceRoot(self):
    result = self._root + '/' + self._appPackageName
    return result
  
  
    
  def urlToQMLResource(self, resourceSubpath):
    '''
    QUrl to a QML resource file.
    For use in QQuickView.setSource(QUrl)
    
    This works whether (regardless) :
    - app is in a normal directory (invoked from Python interpreter)
    - OR app is pyqtdeployed i.e. resources are embedded in a rcc created .qrc file.
    
    URLs referencing embedded files (ie. those whose path starts with ':') 
    need to be prefixed with qrc: rather than file:. 
    fromLocalFile() should handle this automatically - but it doesn't.
    From PyQt mail list.
    
    Assert setResourceRoot() was called earlier.
    
    Assert resourceSubpath does not start with / but ends in .qml.
    E.G. views/bar.qml OR menus/menu.qml
    I.E. resourceSubpath is a subpath of resources/qml/
    '''
    root_url = 'qrc:' if self._root.startswith(':') else self._root
    url = QUrl(root_url + '/' + self._appPackageName + '/resources/qml/' + resourceSubpath)
    print("urlToQMLResource", url)
    return url

    
    
  def pathToAppsMainPackage(self):
    '''
    'resources' should be a subdirectory of main package (not a sibling directory.)
    '''
    result = self._root + '/' + self._appPackageName
    print("Path to apps main package: ", result)
    return result
  
    
  def pathToTranslationResources(self):
    result = self.pathToAppsMainPackage() + 'translations/'
    return result
  
  
resourceMgr = ResourceManager()



"""
CRUFT  because we need a QUrl to QML resources, not a path.
This is code that doesn't work for embedded resources.

def pathToQMLResources(self):
  '''
  QML for the main app.
  Other subsystems may have QML resources in subdirectories such as /resources/qml/style.
  QML resources must be in app's main package in directory /resources/qml/
  
  If using an alternative (compiled resources using pyrcc5, deprecated)
  then pensool_rc.py equals the 'resource' directory, so 'resource' is not a prefix.
  Here, assume resources are a subdirectory of main app package.
  '''
  result = self.pathToAppsMainPackage() + '/resources/qml/'
  print("Path to QML resources: ", result)
  return result
  '''
  FAILS return ":/qml/contextMenus/"  # Qt's notation for file resources (not url)
  FAILS on iOS return config._root + '/resources/qml/contextMenus/'
  '''
  
def _qmlFilenameToQUrl(self,qmlFilename):
  '''
  Convert filename to QUrl.  Assert filename is relative to resources.
  
  Implementation: 
  NOT 'qrc:/'.  See "Managing Resource Files with the Qt Resource System"
  Instead, use as documented for PyQt.
  '''
  qmlUrl=QUrl(qmlFilename)
  assert qmlUrl.isValid()
  #assert qmlUrl.isLocalFile()
  return qmlUrl
"""
  


