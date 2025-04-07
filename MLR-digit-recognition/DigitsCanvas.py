from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class DigitCanvas(QWidget):
    """
    A 28x28 canvas widget where users can draw digits.
    Each cell in the 28x28 grid is displayed larger for easier drawing.
    """
    
    def __init__(self, parent=None, cell_size=10):
        super().__init__(parent)
        
        # Configuration
        self.grid_size = 28
        self.cell_size = cell_size
        self.brush_size = 1
        
        # Set the fixed size based on cell_size
        canvas_size = self.grid_size * self.cell_size
        self.setFixedSize(canvas_size, canvas_size)
        
        # Initialize the image (28x28 grayscale)
        self.image = QImage(self.grid_size, self.grid_size, QImage.Format_Grayscale8)
        self.clear_image()
        
        # Drawing state
        self.drawing = False
        self.last_point = QPoint()
        
        # Appearance
        self.setStyleSheet("background-color: white; border: 1px solid black;")
    
    def clear_image(self):
        """Reset the canvas to blank (white)"""
        self.image.fill(Qt.white)
        self.update()
    
    def paintEvent(self, event):
        """Draw the current image on the widget"""
        painter = QPainter(self)
        
        # Scale the 28x28 image to the widget size
        scaled_image = self.image.scaled(
            self.width(), 
            self.height(),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        painter.drawImage(0, 0, scaled_image)
    
    def to_grid_coordinates(self, screen_x, screen_y):
        """Convert screen coordinates to grid coordinates"""
        x = int(screen_x / self.cell_size)
        y = int(screen_y / self.cell_size)
        
        # Ensure coordinates are within bounds
        x = max(0, min(x, self.grid_size - 1))
        y = max(0, min(y, self.grid_size - 1))
        
        return x, y
    
    def mousePressEvent(self, event):
        """Handle mouse press events to start drawing"""
        if event.button() == Qt.LeftButton:
            x, y = self.to_grid_coordinates(event.position().x(), event.position().y())
            self.last_point = QPoint(x, y)
            self.drawing = True
            self.draw_point(x, y)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events to continue drawing"""
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            x, y = self.to_grid_coordinates(event.position().x(), event.position().y())
            current_point = QPoint(x, y)
            self.draw_line(self.last_point, current_point)
            self.last_point = current_point
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events to stop drawing"""
        if event.button() == Qt.LeftButton:
            self.drawing = False
    
    def draw_point(self, x, y):
        """Draw a single point with anti-aliasing at the specified coordinates"""
        for i in range(-self.brush_size, self.brush_size + 1):
            for j in range(-self.brush_size, self.brush_size + 1):
                nx, ny = x + i, y + j
                
                # Skip if outside the grid
                if not (0 <= nx < self.grid_size and 0 <= ny < self.grid_size):
                    continue
                
                # Calculate intensity based on distance from center (anti-aliasing)
                distance = (i**2 + j**2) ** 0.5
                if distance <= self.brush_size:
                    # Higher intensity (darker) at center, fading to edges
                    intensity = int(max(0, 255 - (255 * (distance / self.brush_size))))
                    self.image.setPixel(nx, ny, 255 - intensity)
        
        self.update()
    
    def draw_line(self, start, end):
        """Draw a line from start to end point using Bresenham's algorithm"""
        x1, y1 = start.x(), start.y()
        x2, y2 = end.x(), end.y()
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        err = dx - dy
        
        while True:
            self.draw_point(x1, y1)
            
            if x1 == x2 and y1 == y2:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    
    def get_image(self):
        """Return the 28x28 image"""
        return self.image
    
    def set_image(self, new_image):
        """Set the canvas image from a QImage"""
        if new_image.size() == QSize(28, 28) and new_image.format() == QImage.Format_Grayscale8:
            self.image = new_image
            self.update()
        else:
            print("Invalid image format. Expected 28x28 grayscale image.")
