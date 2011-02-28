
# For line separator.
import os

# For coordinate calculations.
import math

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import image resources.
import resources

# For QSettings keys.
from settings import SettingsKeys

# For BirthInfo.
from data_objects import BirthInfo

# For conversions from julian day to datetime.datetime and vice versa.
from ephemeris import Ephemeris



class SiderealRadixGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is the circle chart with the following labels on
    the edges:

    - Number for the Rasi
    - Abbreviation for the Nakshatra
    - Number for the Navamsa Rasi.
    """

    def __init__(self, parent=None, scene=None):
        # Logger
        self.log = logging.getLogger("astrologychart.SiderealRadixGraphicsItem")
        self.log.debug("Entered __init__().")

        super().__init__(parent, scene)

        # Pen which is used to do the painting.
        self.pen = QPen()
        self.pen.setColor(QColor(Qt.black))
        self.pen.setWidthF(0.0)
        brush = self.pen.brush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        self.pen.setBrush(brush)
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinates (0, 0) is the center of the widget.  
        # The QRectF returned should be related to this point as the
        # center.

        # TODO:  write code here.
        
        #return QRectF(x, y, width, height)
        return QRectF()

    
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem. """

        if painter.pen() != self.pen:
            painter.setPen(self.pen)

        origin = QPointF(0.0, 0.0)


        ########################################
        # Rasi

        # 30 degrees.
        angleRadians = math.pi / 6.0

        innerRasiRadius = 300.0
        outerRasiRadius = innerRasiRadius + 50.0
        
        # Draw the circles for Rasi.
        painter.drawEllipse(origin, innerRasiRadius, innerRasiRadius)
        painter.drawEllipse(origin, outerRasiRadius, outerRasiRadius)

        # Draw the divisions for Rasi.
        for i in range(0, 12):
            x1 = -1.0 * math.cos(angleRadians * i) * innerRasiRadius
            y1 =  1.0 * math.sin(angleRadians * i) * innerRasiRadius
            x2 = -1.0 * math.cos(angleRadians * i) * outerRasiRadius
            y2 =  1.0 * math.sin(angleRadians * i) * outerRasiRadius
            painter.drawLine(x1, y1, x2, y2)

        # Draw the Rasi labels.
        smallCourierFont = QFont()
        smallCourierFont.setFamily("Lucida Console")
        smallCourierFont.setPointSize(14)

        for i in range(0, 12):
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.4 * angleRadians)
            
            textLocRadius = \
                (0.5 * (outerRasiRadius + innerRasiRadius)) - \
                (0.1 * (outerRasiRadius - innerRasiRadius))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            rotationRadians = (math.pi / 2.0) + textLocAngleRadians
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            textPath.addText(0, 0, smallCourierFont, str(i+1))
            
            rotationTransform = QTransform()
            rotationTransform.translate(x, y)
            rotationTransform.rotate(-1.0 * rotationDegrees)

            rotatedTextPath = QPainterPath()
            rotatedTextPath.addPath(rotationTransform.map(textPath))

            # Change the brush to paint it, then restore the old brush.
            oldBrush = painter.brush()
            painter.setBrush(self.pen.brush())
            painter.drawPath(rotatedTextPath)
            painter.setBrush(oldBrush)

        ########################################
        # Nakshatra
        
        # 13 degrees, 20 minutes.
        angleRadians = (2.0 * math.pi) / 27.0
        
        innerNakshatraRadius = outerRasiRadius
        outerNakshatraRadius = innerNakshatraRadius + 30.0

        painter.drawEllipse(origin, innerNakshatraRadius, innerNakshatraRadius)
        painter.drawEllipse(origin, outerNakshatraRadius, outerNakshatraRadius)

        # Draw the divisions for Nakshatra.
        for i in range(0, 27):
            x1 = -1.0 * math.cos(angleRadians * i) * innerNakshatraRadius
            y1 =  1.0 * math.sin(angleRadians * i) * innerNakshatraRadius
            x2 = -1.0 * math.cos(angleRadians * i) * outerNakshatraRadius
            y2 =  1.0 * math.sin(angleRadians * i) * outerNakshatraRadius
            painter.drawLine(x1, y1, x2, y2)

        # Draw the Nakshatra labels.
        nakshatraAbbrev = ["ASWI",
                           "BHAR",
                           "KRIT",
                           "ROHI",
                           "MRIG",
                           "ARDR",
                           "PUNA",
                           "PUSH",
                           "ASLE",
                           "MAGH",
                           "P PH",
                           "U PH",
                           "HAST",
                           "CHIT",
                           "SWAT",
                           "VISH",
                           "ANUR",
                           "JYES",
                           "MOOL",
                           "P ASH",
                           "U ASH",
                           "SRAV",
                           "DHAN",
                           "SHAT",
                           "P BH",
                           "U BH",
                           "REVA"]

        smallCourierFont = QFont()
        smallCourierFont.setFamily("Lucida Console")
        smallCourierFont.setPointSize(10)

        for i in range(0, 27):
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.3 * angleRadians)
            
            textLocRadius = \
                (0.5 * (outerNakshatraRadius + innerNakshatraRadius)) - \
                (0.3 * (outerNakshatraRadius - innerNakshatraRadius))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            fudgeFactor = \
                (0.01 * textLocAngleRadians)
                        
            rotationRadians = \
                (math.pi / 2.0) + \
                textLocAngleRadians - fudgeFactor
            
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            textPath.addText(0, 0, smallCourierFont, nakshatraAbbrev[i])
            
            rotationTransform = QTransform()
            rotationTransform.translate(x, y)
            rotationTransform.rotate(-1.0 * rotationDegrees)

            rotatedTextPath = QPainterPath()
            rotatedTextPath.addPath(rotationTransform.map(textPath))

            # Change the brush to paint it, then restore the old brush.
            oldBrush = painter.brush()
            painter.setBrush(self.pen.brush())
            painter.drawPath(rotatedTextPath)
            painter.setBrush(oldBrush)
            
            
        ########################################
        # Navamsa
        
        # 13 degrees, 20 minutes.
        angleRadians = (2.0 * math.pi) / (108)
        
        innerNavamsaRadius = outerNakshatraRadius
        outerNavamsaRadius = innerNavamsaRadius + 30.0

        painter.drawEllipse(origin, innerNavamsaRadius, innerNavamsaRadius)
        painter.drawEllipse(origin, outerNavamsaRadius, outerNavamsaRadius)

        # Draw the divisions for Navamsa.
        for i in range(0, 108):
            x1 = -1.0 * math.cos(angleRadians * i) * innerNavamsaRadius
            y1 =  1.0 * math.sin(angleRadians * i) * innerNavamsaRadius
            x2 = -1.0 * math.cos(angleRadians * i) * outerNavamsaRadius
            y2 =  1.0 * math.sin(angleRadians * i) * outerNavamsaRadius
            painter.drawLine(x1, y1, x2, y2)

        # Draw the Navamsa labels.
        smallCourierFont = QFont()
        smallCourierFont.setFamily("Lucida Console")
        smallCourierFont.setPointSize(9)

        for i in range(0, 108):
            rasiNumber = (i + 1) % 12
            if rasiNumber == 0:
                rasiNumber = 12
                
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.3 * angleRadians)
            
            textLocRadius = \
                (0.5 * (outerNavamsaRadius + innerNavamsaRadius)) - \
                (0.3 * (outerNavamsaRadius - innerNavamsaRadius))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            rotationRadians = (math.pi / 2.0) + textLocAngleRadians
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            
            textPath.addText(0, 0, smallCourierFont, str(rasiNumber))
            
            rotationTransform = QTransform()
            rotationTransform.translate(x, y)
            rotationTransform.rotate(-1.0 * rotationDegrees)

            rotatedTextPath = QPainterPath()
            rotatedTextPath.addPath(rotationTransform.map(textPath))

            # Change the brush to paint it, then restore the old brush.
            oldBrush = painter.brush()
            painter.setBrush(self.pen.brush())
            painter.drawPath(rotatedTextPath)
            painter.setBrush(oldBrush)

        
        ########################################
            
        # Two circles for the planet locations.
        innerCircleRadius = outerNavamsaRadius + 30.0
        outerCircleRadius = innerCircleRadius + 30.0

        painter.drawEllipse(origin, innerCircleRadius, innerCircleRadius)
        painter.drawEllipse(origin, outerCircleRadius, outerCircleRadius)


def testSiderealRadixGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")

    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    view.setInteractive(True)

    # Set some rendering settings so things draw nicely.
    view.setRenderHints(QPainter.Antialiasing | 
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform)

    # Set to FullViewportUpdate update mode.
    #
    # The default is normally QGraphicsView.MinimalViewportUpdate, but
    # this caused us to have missing parts of artifacts and missing
    # parts of pricebars.  And while performance isn't as great in
    # the FullViewportUpdate mode, we dont' have many things dynamically
    # updating and changing, so it isn't too big of an issue.
    #view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    
    
    item = SiderealRadixGraphicsItem()
    
    scene.addItem(item)

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()
    
# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect
    
    import sys
    
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
    testSiderealRadixGraphicsItem()

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()
    #app.exec_()
    

        
