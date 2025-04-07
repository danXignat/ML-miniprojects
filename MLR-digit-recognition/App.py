from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import re
import numpy as np

from DigitsCanvas import DigitCanvas
from DataInputDialog import DataInputDialog
from Toolbar import ToolBar


class MNISTDataLoader:
    """
    Class for parsing and loading MNIST-like digit data into the drawing canvas.
    Handles various formats of MNIST data, including the specialized format
    with asterisks and comma separators.
    """
    
    @staticmethod
    def parse_special_format(data_string):
        """
        Parse the special format with asterisks and commas.
        Format example: "0,*0,**0,***0,..." where asterisks are prefixes.
        
        Returns:
            numpy.ndarray: 28x28 array of pixel values (0-255)
        """
        # Clean up the input string
        data_string = data_string.strip()
        
        # Parse the string by handling asterisks and commas
        pattern = r'(\*+)?(\d+)'
        matches = re.findall(pattern, data_string)
        
        # Extract values (ignoring asterisks)
        values = [int(value) for _, value in matches if value]
        
        # Ensure we have 784 values (28x28)
        if len(values) < 784:
            values.extend([0] * (784 - len(values)))
        elif len(values) > 784:
            values = values[:784]
            
        # Reshape to 28x28
        pixel_array = np.array(values, dtype=np.uint8).reshape(28, 28)
        
        return pixel_array
    
    @staticmethod
    def parse_csv_format(data_string):
        """
        Parse standard CSV format where values are comma-separated.
        
        Returns:
            numpy.ndarray: 28x28 array of pixel values (0-255)
        """
        # Split by commas and convert to integers
        values = [int(val) for val in data_string.strip().split(',') if val]
        
        # Ensure we have 784 values
        if len(values) < 784:
            values.extend([0] * (784 - len(values)))
        elif len(values) > 784:
            values = values[:784]
            
        # Reshape to 28x28
        pixel_array = np.array(values, dtype=np.uint8).reshape(28, 28)
        
        return pixel_array
    
    @staticmethod
    def array_to_qimage(pixel_array):
        """
        Convert a numpy array to a QImage that can be displayed in the canvas.
        
        Args:
            pixel_array: 28x28 numpy array of pixel values
            
        Returns:
            QImage: 28x28 grayscale image
        """
        height, width = pixel_array.shape
        image = QImage(width, height, QImage.Format_Grayscale8)
        
        # Set pixel values
        for y in range(height):
            for x in range(width):
                pixel_value = pixel_array[y, x]
                image.setPixel(x, y, pixel_value)
        
        return image

class App(QMainWindow):
    """Main application window for digit drawing"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("28x28 Digit Drawing App")
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface components"""
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Drawing canvas
        self.canvas = DigitCanvas()
        
        # Toolbar
        self.toolbar = ToolBar()
        self.toolbar.clear_button.clicked.connect(self.canvas.clear_image)
        self.toolbar.save_button.clicked.connect(self.save_image)
        self.toolbar.load_button.clicked.connect(self.load_data)
        
        # Add widgets to main layout
        main_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.toolbar)
        
        # Size the window appropriately
        self.adjustSize()
    
    def save_image(self):
        """Save the drawn digit image with a file dialog"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Digit Image",
            "digit.png",
            "PNG Images (*.png);;All Files (*)"
        )
        
        if file_path:
            # Get the 28x28 image
            image = self.canvas.get_image()
            image.save(file_path)
            print(f"Image saved as '{file_path}'")
    
    def load_data(self):
        """Load MNIST data from text input"""
        dialog = DataInputDialog(self)
        
        if dialog.exec():
            data_string, is_special_format = dialog.get_data()
            
            try:
                # Parse data based on selected format
                if is_special_format:
                    pixel_array = MNISTDataLoader.parse_special_format(data_string)
                else:
                    pixel_array = MNISTDataLoader.parse_csv_format(data_string)
                
                # Convert to QImage
                image = MNISTDataLoader.array_to_qimage(pixel_array)
                
                # Set the image in the canvas
                self.canvas.set_image(image)
                
                print("Data loaded successfully")
                
            except Exception as e:
                print(f"Error loading data: {e}")
