
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class ColorIcon(QIcon):
    """A QIcon hosting just a color."""
    
    def __init__(self, color=None):
        """Initializes a QIcon with a certain color.
        
        Arguments:
            color - QColor object representing the color to set the text.
        """


        # Internally stored QColor object.
        self.color = color

        if color == None:
            self.color = QColor()

        self.pixmap = QPixmap(QSize(32, 32))
        self.pixmap.fill(self.color)

        super().__init__(self.pixmap)

    def getColor(self):
        """Returns the current QColor setting of this widget.  This value
        may be None if no color was set previously.
        """

        return self.color

        
class ColorEditPushButton(QPushButton):
    """A QPushButton but with a color and text."""

    def __init__(self, color=None, text="Edit"):

        super().__init__(ColorIcon(color), text)

        self.color = color

    def setColor(self, color):
        """Sets the color of held by this widget.

        Arguments:
            color - QColor object representing the new color to use for
                    this widget.  Cannot be None.
        """

        if color != None and self.color != color:
            self.color = color
            self.setIcon(ColorIcon(self.color))

    def getColor(self):
        """Returns the current QColor setting of this widget.  This value
        may be None if no color was set previously.
        """

        return self.color



