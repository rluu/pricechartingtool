
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

class ColorLabel(QLabel):
    """QLabel that holds just a color."""

    def __init__(self, color=None):
        """Initializes the widget with a certain color.
        
        Arguments:
            color - QColor object representing the color to set.
        """

        super().__init__()

        # Default width and height for the pixmap.
        self.pixmapWidth = 32
        self.pixmapHeight = 32

        # Internally stored QColor object.
        self.color = color

        if color == None:
            self.color = QColor()

        self.setColor(self.color)

    def getColor(self):
        """Returns the current QColor setting of this widget.  This value
        may be None if no color was set previously.
        """

        return self.color

    def setColor(self, color):
        """Sets the color.
        """

        self.color = color

        if color == None:
            self.color = QColor()
                
        pixmap = QPixmap(QSize(self.pixmapWidth, self.pixmapHeight))
        pixmap.fill(self.color)

        self.setPixmap(pixmap)


    def setDimensions(self, width=32, height=32):
        """Sets the width and height of the QPixmap used for the label.
        Arguments:
        width - int value for the width.
        height - int value for the height.
        """
        
        # Set the variables.
        self.pixmapWidth = width
        self.pixmapHeight = height
        
        # Re-set the color to apply the changes in pixmap size.
        self.setColor(self.color)


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


def qColorToStr(qcolor):
    """Returns a string formatting of a QColor object."""

    return "QColor(h={},s={},v={},r={},g={},b={},a={})".\
           format(qcolor.hue(),
                  qcolor.saturation(),
                  qcolor.value(),
                  qcolor.red(),
                  qcolor.green(),
                  qcolor.blue(),
                  qcolor.alpha())

def testColorIcon():
    print("Running " + inspect.stack()[0][3] + "()")

    colorIcon1 = ColorIcon(QColor(Qt.red))
    colorIcon2 = ColorIcon(QColor(Qt.blue))
    colorIcon3 = ColorIcon(QColor(Qt.green))
    colorIcon4 = ColorIcon()
    colorIcon5 = ColorIcon(QColor(Qt.yellow))

    colorIcons = [colorIcon1, 
                  colorIcon2, 
                  colorIcon3, 
                  colorIcon4, 
                  colorIcon5
                  ]
    
    # TODO: Create a test for ColorIcon().  The below doesn't work.  How do I get Qt to display the Icons only?

    #for colorIcon in colorIcons:
    #    layout = QVBoxLayout()
    #    layout.addWidget(colorIcon)
    # 
    #    dialog = QDialog()
    #    dialog.setLayout(layout)
    #    rv = dialog.exec_()


def testColorLabel():
    print("Running " + inspect.stack()[0][3] + "()")

    colorLabel1 = ColorLabel(QColor(Qt.red))
    colorLabel2 = ColorLabel(QColor(Qt.blue))
    colorLabel3 = ColorLabel(QColor(Qt.green))
    colorLabel4 = ColorLabel(QColor())          # Displays black.
    colorLabel5 = ColorLabel()                  # Displays black.
    colorLabel6 = ColorLabel(QColor(Qt.yellow))

    colorLabels = [colorLabel1, 
                   colorLabel2, 
                   colorLabel3,
                   colorLabel4,
                   colorLabel5,
                   colorLabel6,
                   ]

    for colorLabel in colorLabels:
        layout = QVBoxLayout()
        layout.addWidget(colorLabel)
    
        dialog = QDialog()
        dialog.setLayout(layout)
        rv = dialog.exec_()

def testColorEditPushButton():
    print("Running " + inspect.stack()[0][3] + "()")
    
    color = QColor(Qt.red)

    print("Color before: {}".format(qColorToStr(color)))

    button = ColorEditPushButton(color)

    layout = QVBoxLayout()
    layout.addWidget(button)
    
    dialog = QDialog()
    dialog.setLayout(layout)
    rv = dialog.exec_()

    button.getColor()
    
    # Strangely, the color changed by clicking the ColorEditPushButton doesn't
    # get retained in the button after the dialog closes.  Why?  This shouldn't
    # have an impact on the way I use this widget, but it may have an impact in
    # the future.

    print("Color  after: {}".format(qColorToStr(color)))


# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect
    
    # Initialize the Ephemeris (required).
    #Ephemeris.initialize()

    # Set a default location (required).
    #Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)


    # Various tests to run:
    #testColorIcon()
    #testColorLabel()
    testColorEditPushButton()

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    #app.exec_()

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()


