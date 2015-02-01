
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
      result = self._searchForRootWindow()
    assert result is not None, "None top level window."
    print("App's single QWindow:", result)
    self._topLevelWindow = result
    return result


  def _searchForRootWindow(self):
    '''
    Iterate through top windows, finding first one of class QWindow.
    Any others should be QQuickWindows (for displaying QML.)
    '''
    result = None
    qwinList = QGuiApplication.topLevelWindows()
    print("topLevelWindows():")
    for win in qwinList:
      print("window: ", win)
      if win.__class__ == 'QWindow':
        result = win
        break
    return result
      
  
  
  def getRootWindow(self):
    '''
    Get root window found earlier.
    '''
    result = self._topLevelWindow
    assert result is not None, "Top window found earlier."
    return result
  
  
windowMgr = WindowManager()
