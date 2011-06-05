
# For directory access.
import os
import sys

# For logging.
import logging
import logging.config

# For PyQt widgets.
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

        self.clicked.connect(self._handleButtonClicked)

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

    def _handleButtonClicked(self):
        """Brings up a color QColorDialog to edit the current color.
        If the new color is valid and it is a different color, then we
        set the button as having the new color.
        """

        # First get the current color.
        currColor = self.getColor()

        # Open a dialog to obtain a new color.
        newColor = QColorDialog.getColor(currColor)

        # If a color was chosen that is different, then set the new color.
        if newColor.isValid() and currColor != newColor:
            self.setColor(newColor)



# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect
    
    # Initialize the Ephemeris (required).
    Ephemeris.initialize()

    # Set a default location (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)


    # Various tests to run:
    # -
        
    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    #app.exec_()

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()


