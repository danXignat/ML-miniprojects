from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class DataInputDialog(QDialog):
    """Dialog for inputting MNIST data in various formats"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Load MNIST Data")
        self.setMinimumSize(500, 300)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Paste MNIST digit data below. Data can be in standard CSV format "
            "or the special format with asterisks."
        )
        instructions.setWordWrap(True)
        
        # Text input
        self.text_input = QTextEdit()
        
        # Format selection
        self.format_label = QLabel("Select data format:")
        
        format_layout = QHBoxLayout()
        self.standard_button = QPushButton("Standard CSV")
        self.special_button = QPushButton("Special Format (with *)")
        
        format_layout.addWidget(self.standard_button)
        format_layout.addWidget(self.special_button)
        
        # Connect buttons
        self.standard_button.clicked.connect(self.accept_standard)
        self.special_button.clicked.connect(self.accept_special)
        
        # Add widgets to layout
        layout.addWidget(instructions)
        layout.addWidget(self.text_input)
        layout.addWidget(self.format_label)
        layout.addLayout(format_layout)
        
        # Data format flag
        self.is_special_format = False
    
    def accept_standard(self):
        """Accept with standard CSV format"""
        self.is_special_format = False
        self.accept()
    
    def accept_special(self):
        """Accept with special format (asterisks)"""
        self.is_special_format = True
        self.accept()
    
    def get_data(self):
        """Return the input text and format flag"""
        return self.text_input.toPlainText(), self.is_special_format