from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class ToolBar(QWidget):
    """Toolbar with buttons for actions like clear and save"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create buttons
        self.clear_button = QPushButton("Clear")
        self.save_button = QPushButton("Save")
        self.load_button = QPushButton("Load Data")
        
        # Add buttons to layout
        layout.addWidget(self.clear_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)