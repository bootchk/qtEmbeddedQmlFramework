
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
#from PyQt5.QtCore import QSignalMapper
 
 

class QmlDelegate(QObject):
  '''
  Delegate between QML (view) and Python (model.)
  Typically for a QML dialog.
  
  A type that will be registered with QML.  
  Must be a sub-class of QObject.
  
  Use cases:
    - Delegate is an empty model (i.e. accept or cancel is the only dataflow.): use QmlDelegate directly.
      I.E. a message dialog.
    - Delegate is a model having properties and the UI is a dialog that edits the properties: use QmlDelegate as a Mixin
  '''
  
  #activated = Signal()
  openView = Signal() # to QML view
  accepted = Signal() # to model
  rejected = Signal() # to model
  
  '''
  Note connections (for instances) can be made from QML or from Python?
  
  Method must be slot to be callable/invokeable from QML JS.
  '''

  " __init__ automatically flows through to QObject "
  
  
  
  def emitOpenView(self):
    '''
    Activate view of self (self as a model.)
    Called from business side.
    Connected in QML to Dialog.open()
    '''
    print("activate called, emitting openView")
    self.openView.emit()
  
  '''
  Alias
  From business side, open means "window modal."
  That semantic must be defined in the QML.
  '''
  open = emitOpenView
  
  
  @Slot()
  def accept(self):
    '''
    Called from QML side.
    Connected in business side to a handler of dialog results (in shared model.)
    '''
    self.accepted.emit()
  
  @Slot()
  def reject(self):
    '''
    Opposite cohort of accept.
    '''
    self.rejected.emit()
    