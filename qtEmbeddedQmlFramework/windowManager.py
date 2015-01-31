
from PyQt5.QtGui import QGuiApplication

class WindowManager():
  '''
  Knows top level QWindow of app.
  Needed to transientParent a QQuickView to app QWindow.
  After you create QQuickViews, they too will be top level.
  
  The ordering of QQuickViews is via their transientParent, not via the OS's window manager ordering.
  That is, especially on mobile devices, windows don't have a containment parent/child relation, they are all top-level.
  '''
  
  def findRootWindow(self):
    '''
    Find and remember a distinguished top window of the app.
    Should be called during app init when you expect only one window to exist.
    '''
    qwinList = QGuiApplication.topLevelWindows()
    print("window count", len(qwinList))
    
    if len(qwinList)==1:
      result = qwinList[0]
    else:
      # Raise exception? 
      result = None
    print("App's single QWindow:", result)
    
    """
    ALTERNATIVE?  Search for a single window of type QWindow?
    
    print("topLevelWindows():")
    for win in qwinList:
      print("window: ", win)
    """
    self._topLevelWindow = result
    return result


  def getRootWindow(self):
    '''
    Get root window found earlier.
    '''
    result = self._topLevelWindow
    assert result is not None, "Top window found earlier."
    return result
  
  
windowMgr = WindowManager()
