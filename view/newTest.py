import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget, QStyle
from qfluentwidgets import ToolButton, NavigationInterface, RadioButton, NavigationItemPosition, Theme, setTheme, setThemeColor
from qframelesswindow import FramelessWindow, StandardTitleBar
from qfluentwidgets import FluentIcon as FIF






class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))
        setTheme(Theme.LIGHT)   
        
        
        self.nav = NavigationInterface(showMenuButton= True)
        self.stack = QStackedWidget(self)
        
        self.stack.setStyleSheet("background-color: #40434a; color: white;")
        self.radio = RadioButton()
        self.stack.addWidget(self.radio)
        
       
        
        self.nav.addItem(self.radio.objectName(), icon=FIF.ACCEPT_MEDIUM,text="ciao bela", position= NavigationItemPosition.TOP)
        
        
      
        self.setWindowTitle("first attempt")
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.layout.addWidget(self.nav)
        self.layout.addWidget(self.stack)
        self.layout.setStretchFactor(self.stack, 1)
        
        
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = Window()
    window.show()
    app.exec_()
