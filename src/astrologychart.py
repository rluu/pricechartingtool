
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


class RadixChartGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is the circle astrology chart."""

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

    def getRadiusForWheelNumber(self, wheelNumber):
        """Virtual function.  Subclasses must overwrite and implement.

        Returns the radius of the circle drawn for the argument wheel
        number.  This value is used by child QGraphicsItems to
        determine where they should be drawn for a certain wheel
        number.  The first wheel is wheel number 0.

        Argument:
        wheelNumber - int value for the wheel number.

        Returns:
        float - value for the radius of that wheel number.
        """

        return 0.0

    def getTerminalRadiusForWheelNumber(self, wheelNumber):
        """Virtual function.  Subclasses must overwrite and implement.

        Returns the radius from the origin of where the terminal line
        of child items should terminate for a certain wheel number.
        The returned value is less than the number returned from the
        call to getRadiusForWheelNumber().  The first wheel is wheel
        number 0.

        Argument:
        wheelNumber - int value for the wheel number.

        Returns:
        float - value for the radius.
        """

        return 0.0

class SiderealRadixChartGraphicsItem(RadixChartGraphicsItem):
    """QGraphicsItem that is the circle chart with the following labels on
    the edges:

    - Number for the Rasi
    - Abbreviation for the Nakshatra
    - Number for the Navamsa Rasi.
    """

    def __init__(self, parent=None, scene=None):
        # Logger
        self.log = \
            logging.getLogger("astrologychart.SiderealRadixChartGraphicsItem")

        super().__init__(parent, scene)

        # Pen which is used to do the painting.
        self.pen = QPen()
        self.pen.setColor(QColor(Qt.black))
        self.pen.setWidthF(0.0)
        brush = self.pen.brush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        self.pen.setBrush(brush)

        # Below are radius measurements for when drawing.
        
        # Rasi
        self.innerRasiRadius = 300.0
        self.outerRasiRadius = self.innerRasiRadius + 50.0

        # Nakshatra
        self.innerNakshatraRadius = self.outerRasiRadius
        self.outerNakshatraRadius = self.innerNakshatraRadius + 30.0

        # Navamsa
        self.innerNavamsaRadius = self.outerNakshatraRadius
        self.outerNavamsaRadius = self.innerNavamsaRadius + 30.0

        # Circles for the planet locations.
        increment = 52.0
        i = 0
        self.wheelNumberCircleRadius = list()
        self.wheelNumberCircleRadius.\
            append(self.outerNavamsaRadius + increment)
        i += 1
        self.wheelNumberCircleRadius.\
            append(self.wheelNumberCircleRadius[i-1] + increment)
        i += 1
        self.wheelNumberCircleRadius.\
            append(self.wheelNumberCircleRadius[i-1] + increment)
        i += 1
        self.wheelNumberCircleRadius.\
            append(self.wheelNumberCircleRadius[i-1] + increment)

        # Below are the fonts used in drawing text.
        self.rasiLabelFont = QFont()
        self.rasiLabelFont.setFamily("Lucida Console")
        self.rasiLabelFont.setPointSize(14)

        self.nakshatraLabelFont = QFont()
        self.nakshatraLabelFont.setFamily("Lucida Console")
        self.nakshatraLabelFont.setPointSize(10)

        self.navamsaLabelFont = QFont()
        self.navamsaLabelFont.setFamily("Lucida Console")
        self.navamsaLabelFont.setPointSize(9)

    def getRadiusForWheelNumber(self, wheelNumber):
        """Overwritten function from class RadixChartGraphicsItem.

        Returns the radius of the circle drawn for the argument wheel
        number.  This value is used by child QGraphicsItems to
        determine where they should be drawn for a certain wheel
        number.  The first wheel is wheel number 0.

        Argument:
        wheelNumber - int value for the wheel number.

        Returns:
        float - value for the radius of that wheel number.
        """

        # Return value.
        rv = 0.0
        
        if wheelNumber >= 0 and wheelNumber < len(self.wheelNumberCircleRadius):
            rv = self.wheelNumberCircleRadius[wheelNumber]
        else:
            self.log.error("Invalid wheelNumber provided to " + \
                           "getRadiusForWheelNumber().  Returning 0.0")
            rv = 0.0

        return rv

    def getTerminalRadiusForWheelNumber(self, wheelNumber):
        """Overwritten function from class RadixChartGraphicsItem.

        Returns the radius from the origin of where the terminal line
        of child items should terminate for a certain wheel number.
        The returned value is less than the number returned from the
        call to getRadiusForWheelNumber().  The first wheel is wheel
        number 0.

        Argument:
        wheelNumber - int value for the wheel number.

        Returns:
        float - value for the radius.
        """

        # Return value.
        rv = 0.0

        # TODO:  decide if I should keep it at 0.0.
        return rv
    
        if wheelNumber >= 1 and wheelNumber < len(self.wheelNumberCircleRadius):
            rv = self.wheelNumberCircleRadius[wheelNumber - 1]
        elif wheelNumber == 0:
            rv = self.outerNavamsaRadius
        else:
            self.log.error("Invalid wheelNumber provided to " + \
                           "getTerminalRadiusForWheelNumber().  Returning 0.0")
            rv = 0.0

        return rv

    def getInnerRasiRadius(self):
        """Returns the radius of the inner Rasi circle."""
        
        return self.innerRasiRadius

    def getOuterRasiRadius(self):
        """Returns the radius of the outer Rasi circle."""

        return self.outerRasiRadius

    def getInnerNakshatraRadius(self):
        """Returns the radius of the inner Nakshatra circle."""
        
        return self.innerNakshatraRadius

    def getOuterNakshatraRadius(self):
        """Returns the radius of the outer Nakshatra circle."""

        return self.outerNakshatraRadius
    
    def getInnerNavamsaRadius(self):
        """Returns the radius of the inner Navamsa circle."""
        
        return self.innerNavamsaRadius

    def getOuterNavamsaRadius(self):
        """Returns the radius of the outer Navamsa circle."""

        return self.outerNavamsaRadius
    
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) is the center of the widget.  
        # The painting should be relative to this point as the
        # center.


        # If there are circles for where the planets are drawn (which
        # there should be), then set the radius as the last circle
        # drawn.  This is the one with the largest radius.
        radius = 0.0
        if len(self.wheelNumberCircleRadius) > 0:
            radius = self.wheelNumberCircleRadius[-1]
            
        diameter = radius + radius
        
        x = -1.0 * radius
        y = -1.0 * radius
        width = diameter
        height = diameter
        
        return QRectF(x, y, width, height)
    
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem. """

        if painter.pen() != self.pen:
            painter.setPen(self.pen)

        # Coordinate (0, 0) is the center of the widget.  
        # The painting should be relative to this point as the
        # center.

        origin = QPointF(0.0, 0.0)


        ########################################
        # Rasi

        # 30 degrees.
        angleRadians = math.pi / 6.0

        # Draw the circles for Rasi.
        painter.drawEllipse(origin, self.innerRasiRadius, self.innerRasiRadius)
        painter.drawEllipse(origin, self.outerRasiRadius, self.outerRasiRadius)

        # Draw the divisions for Rasi.
        for i in range(0, 12):
            x1 = -1.0 * math.cos(angleRadians * i) * self.innerRasiRadius
            y1 =  1.0 * math.sin(angleRadians * i) * self.innerRasiRadius
            x2 = -1.0 * math.cos(angleRadians * i) * self.outerRasiRadius
            y2 =  1.0 * math.sin(angleRadians * i) * self.outerRasiRadius
            painter.drawLine(x1, y1, x2, y2)

        # Draw the Rasi labels.
        for i in range(0, 12):
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.4 * angleRadians)
            
            textLocRadius = \
                ((0.5 * (self.outerRasiRadius + self.innerRasiRadius)) -
                 (0.1 * (self.outerRasiRadius - self.innerRasiRadius)))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            rotationRadians = (math.pi / 2.0) + textLocAngleRadians
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            textPath.addText(0, 0, self.rasiLabelFont, str(i+1))
            
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
        
        painter.drawEllipse(origin,
                            self.innerNakshatraRadius,
                            self.innerNakshatraRadius)
        painter.drawEllipse(origin,
                            self.outerNakshatraRadius,
                            self.outerNakshatraRadius)

        # Draw the divisions for Nakshatra.
        for i in range(0, 27):
            x1 = -1.0 * math.cos(angleRadians * i) * self.innerNakshatraRadius
            y1 =  1.0 * math.sin(angleRadians * i) * self.innerNakshatraRadius
            x2 = -1.0 * math.cos(angleRadians * i) * self.outerNakshatraRadius
            y2 =  1.0 * math.sin(angleRadians * i) * self.outerNakshatraRadius
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

        for i in range(0, 27):
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.3 * angleRadians)
            
            textLocRadius = \
                ((0.5 * (self.outerNakshatraRadius +
                         self.innerNakshatraRadius)) -
                 (0.3 * (self.outerNakshatraRadius -
                         self.innerNakshatraRadius)))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            fudgeFactor = \
                (0.01 * textLocAngleRadians)
                        
            rotationRadians = \
                (math.pi / 2.0) + \
                textLocAngleRadians - fudgeFactor
            
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            textPath.addText(0, 0, self.nakshatraLabelFont, nakshatraAbbrev[i])
            
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
        
        painter.drawEllipse(origin,
                            self.innerNavamsaRadius,
                            self.innerNavamsaRadius)
        painter.drawEllipse(origin,
                            self.outerNavamsaRadius,
                            self.outerNavamsaRadius)

        # Draw the divisions for Navamsa.
        for i in range(0, 108):
            x1 = -1.0 * math.cos(angleRadians * i) * self.innerNavamsaRadius
            y1 =  1.0 * math.sin(angleRadians * i) * self.innerNavamsaRadius
            x2 = -1.0 * math.cos(angleRadians * i) * self.outerNavamsaRadius
            y2 =  1.0 * math.sin(angleRadians * i) * self.outerNavamsaRadius
            painter.drawLine(x1, y1, x2, y2)

        # Draw the Navamsa labels.
        for i in range(0, 108):
            rasiNumber = (i + 1) % 12
            if rasiNumber == 0:
                rasiNumber = 12
                
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.3 * angleRadians)
            
            textLocRadius = \
                ((0.5 * (self.outerNavamsaRadius + self.innerNavamsaRadius)) -
                 (0.3 * (self.outerNavamsaRadius - self.innerNavamsaRadius)))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            rotationRadians = (math.pi / 2.0) + textLocAngleRadians
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            
            textPath.addText(0, 0, self.navamsaLabelFont, str(rasiNumber))
            
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
        for i in range(len(self.wheelNumberCircleRadius)):
            painter.drawEllipse(origin,
                                self.wheelNumberCircleRadius[i],
                                self.wheelNumberCircleRadius[i])

class RadixPlanetGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is a 'planet' to be drawn with a
    RadixChartGraphicsItem object as its parent QGraphicsItem.
    """

    def __init__(self,
                 planetGlyphUnicode,
                 planetGlyphFontSize,
                 planetAbbreviation,
                 planetForegroundColor,
                 planetBackgroundColor,
                 degree = 0.0,
                 velocity = 0.0,
                 wheelNumber = 0,
                 parent=None,
                 scene=None):
        """Initializes the object with the given arguments.

        Arguments:
        planetGlyphUnicode - str holding the planet glyph.
        planetGlyphUnicode - float font size for drawing the glyph.
        planetAbbreviation - str holding the planet abbreviation.
        planetForegroundColor - QColor object for the foreground color to
                                be used for the drawing of the planet.
        planetBackgroundColor - QColor object for the background color to
                                be used for the drawing of the planet.
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        wheelNumber - int value for the wheel number to draw the planet on.
                      The first wheel (circle) is wheel number 0.
        parent - RadixChartGraphicsItem that is the parent for this
                 QGraphicsItem.
        scene - QGraphicsScene object to draw this QGraphicsItem on.
        """
    
        # Logger
        self.log = \
            logging.getLogger("astrologychart.RadixPlanetGraphicsItem")

        super().__init__(parent, scene)

        # Save the parameter values.
        self.planetGlyphUnicode = planetGlyphUnicode
        self.planetGlyphFontSize = planetGlyphFontSize
        self.planetAbbreviation = planetAbbreviation
        self.planetForegroundColor = planetForegroundColor
        self.planetBackgroundColor = planetBackgroundColor
        self.degree = degree
        self.velocity = velocity
        self.wheelNumber = wheelNumber
        self.radixChartGraphicsItem = parent

        # Get the retrograde symbol.
        # (Below is commented out because we're using parenthesis instead).
        #settings = QSettings()
        #self.planetRetrogradeGlyphUnicode = \
        #    settings.value(SettingsKeys.planetRetrogradeGlyphUnicodeKey,
        #                   SettingsKeys.planetRetrogradeGlyphUnicodeDefValue)
        #self.planetRetrogradeGlyphFontSize = \
        #    settings.value(SettingsKeys.planetRetrogradeGlyphFontSizeKey,
        #                   SettingsKeys.planetRetrogradeGlyphFontSizeDefValue)
        
        # Radius from the origin to draw this planet.
        self.drawPointRadius = 0.0
        self.drawPointTerminalRadius = 0.0

        # Call our overwritten self.setParentItem() manually so that
        # the parent object type can be verified.  This will also
        # subsequently have the (desired) side effect of
        # re-calculating the radisuses above.
        self.setParentItem(parent)

        
    def setParentItem(self, parent):
        """Overwrites QGraphicsItem.setParentItem().  Needed so we can
        save off the parent in self.radixChartGraphicsItem.

        Arguments:
        parent - RadixChartGraphicsItem parent object.
        """

        # Verify parent class.
        if parent != None and not isinstance(parent, RadixChartGraphicsItem):
            raise TypeError("Argument 'parent' is not of type " + \
                            "'RadixChartGraphicsItem'")
        
        # Save off the parent.
        self.radixChartGraphicsItem = parent

        # Call self.setWheelNumber() again so the radiuses can be recalculated.
        self.setWheelNumber(self.wheelNumber)
        
    def setDegree(self, degree):
        """Sets the location of the planet in degrees of the zodiac.

        Arguments:
        
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        """

        self.degree = degree
        self.update()
        
    def getDegree(self):
        """Returns the location of the planet in degrees of the zodiac.

        Returns:
        float - Value representing the degree location of the planet.
                The value returned will be between: [0.0, 360).
        """

        return self.degree

    def setVelocity(self, velocity):
        """Sets the velocity of the planet, in degrees per day.

        Arguments:
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.velocity = velocity
        self.update()

    def getVelocity(self):
        """Returns the velocity of the planet, in degrees per day.

        Returns:
        float - Value for the velocity of the planet, in degrees
                per day.
        """

        return self.velocity

    def setDegreeAndVelocity(self, degree, velocity):
        """Sets the degree location of the planet and the velocity of
        the planet, all at once.

        Arguments:
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.degree = degree
        self.velocity = velocity

        self.update()
        
    def setWheelNumber(self, wheelNumber):
        """Sets the wheel number that it will be drawn on.
        This value represents which 'circle' to use on
        RadixChartGraphicsItem for drawing the planet.
        The first wheel (circle) is wheel number 0.
        
        Arguments:
        wheelNumber - int value for the wheel number to draw the planet on.
                      The first wheel (circle) is wheel number 0.
        """

        self.wheelNumber = wheelNumber

        # Update the radius location point if we have a parent radix chart set.
        if self.radixChartGraphicsItem != None:
            drawPointRadius = \
                self.radixChartGraphicsItem.\
                getRadiusForWheelNumber(self.wheelNumber)
            drawPointTerminalRadius = \
                self.radixChartGraphicsItem.\
                getTerminalRadiusForWheelNumber(self.wheelNumber)

            # Update variables only if new values are different.
            if self.drawPointRadius != drawPointRadius or \
               self.drawPointTerminalRadius != drawPointTerminalRadius:
                
                self.drawPointRadius = drawPointRadius
                self.drawPointTerminalRadius = drawPointTerminalRadius
                
                self.update()

    def getWheelNumber(self):
        """Returns the wheel number that the planet is drawn on.
        This value represents which 'circle' to use on
        RadixChartGraphicsItem for drawing the planet.
        The first wheel (circle) is wheel number 0.

        Returns:
        int - Value representing which wheel number the planet is drawn on.
              A value of 0 indicates the first wheel from the center.
        """

        return self.wheelNumber

    def getPlanetGlyphUnicode(self):
        """Returns the planet glyph in unicode."""

        return self.planetGlyphUnicode

    def getPlanetGlyphFontSize(self):
        """Returns the planet glyph font size."""

        return self.planetGlyphFontSize

    def getPlanetAbbreviation(self):
        """Returns the planet abbreviation."""

        return self.planetAbbreviation

    def getPlanetForegroundColor(self):
        """Returns the planet foreground color as a QColor object."""

        return self.planetForegroundColor

    def getPlanetBackgroundColor(self):
        """Returns the planet background color as a QColor object."""

        return self.planetBackgroundColor

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem.

        We implement this function by taking all the pieces, and doing
        an logical OR on the areas covered by their rectangles.  The
        rectangles are calculated in the same way that paint() is
        done.  Changes to paint() will required changes to this
        method.
        """

        # QRectF for the line.
        x1 = -1.0 * math.cos(math.radians(self.degree)) * \
             self.drawPointRadius
        y1 =  1.0 * math.sin(math.radians(self.degree)) * \
             self.drawPointRadius
        x2 = -1.0 * math.cos(math.radians(self.degree)) * \
             self.drawPointTerminalRadius
        y2 =  1.0 * math.sin(math.radians(self.degree)) * \
             self.drawPointTerminalRadius
        lineRect = QRectF(QPointF(x1, y1), QPointF(x2, y2)).normalized()

        # QRectF for the planet glyph text.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)
        text = self.planetGlyphUnicode
        if self.velocity < 0:
            text = "(" + self.planetGlyphUnicode + ")"
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        rotationTransform = QTransform()
        fudgeDegrees = 0.5
        rotationDegrees = self.degree + fudgeDegrees
        r = self.radixChartGraphicsItem.\
            getRadiusForWheelNumber(self.wheelNumber + 1)
        planetTextRadius = r - ((r - self.drawPointRadius) / 3.0)
        textX = -1.0 * math.cos(math.radians(rotationDegrees)) * \
                planetTextRadius
        textY = 1.0 * math.sin(math.radians(rotationDegrees)) * \
                planetTextRadius
        rotationTransform.translate(textX, textY)
        rotationTransform.rotate(-1.0 * (self.degree + 90))

        rotatedTextPath = QPainterPath()
        rotatedTextPath.addPath(rotationTransform.map(textPath))
        planetTextRect = rotatedTextPath.boundingRect()

        # QRectF for the planet degree location text.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)
        # Normalize degree value.
        degreesInSign = self.degree
        while degreesInSign < 0:
            degreesInSign += 360.0
        while degreesInSign >= 360.0:
            degreesInSign -= 360.0
        # Get integer values of degrees and minutes.
        minutesInDegree = \
            int((degreesInSign - math.floor(degreesInSign)) * 60.0)
        degreesInSign = int(math.floor(degreesInSign))
        # Text.
        text = "{}\u00b0{}'".format(degreesInSign, minutesInDegree)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        rotationTransform = QTransform()
        fudgeDegrees = 1.0
        rotationDegrees = self.degree + fudgeDegrees
        r = self.radixChartGraphicsItem.\
            getRadiusForWheelNumber(self.wheelNumber + 1)
        planetTextRadius = r - (2.0 * (r - self.drawPointRadius) / 3.0)
        textX = -1.0 * math.cos(math.radians(rotationDegrees)) * \
                planetTextRadius
        textY = 1.0 * math.sin(math.radians(rotationDegrees)) * \
                planetTextRadius
        rotationTransform.translate(textX, textY)
        rotationTransform.rotate(-1.0 * (self.degree + 90))
        rotatedTextPath = QPainterPath()
        rotatedTextPath.addPath(rotationTransform.map(textPath))
        planetDegreeTextRect = rotatedTextPath.boundingRect()
        

        # Unite all rectangles.
        rv = lineRect.united(planetTextRect).united(planetDegreeTextRect)
        
        return rv

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.
        
        The painting is done in three parts:
        - Paint the line from the text to the terminal point.
        - Paint the planet glyph as text.
        - Paint the degree location as text.

        Note: boundingRect() utilizes the same calculations as here,
        so if this function changes, then boundingRect() will need to
        be updated as well.
        """

        # Change the brush and pen in the painter.
        # We will restore it when done.
        oldBrush = painter.brush()
        oldPen = painter.pen()
        pen = painter.pen()
        pen.setColor(QColor(self.planetForegroundColor))
        pen.setWidthF(0.0)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(self.planetForegroundColor)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw the line.
        x1 = -1.0 * math.cos(math.radians(self.degree)) * \
             self.drawPointRadius
        y1 =  1.0 * math.sin(math.radians(self.degree)) * \
             self.drawPointRadius

        x2 = -1.0 * math.cos(math.radians(self.degree)) * \
             self.drawPointTerminalRadius
        y2 =  1.0 * math.sin(math.radians(self.degree)) * \
             self.drawPointTerminalRadius

        painter.drawLine(x1, y1, x2, y2)

        # Draw the text for the planet.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)

        text = self.planetGlyphUnicode
        if self.velocity < 0:
            text = "(" + self.planetGlyphUnicode + ")"
            
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        
        rotationTransform = QTransform()
        fudgeDegrees = 0.5
        rotationDegrees = self.degree + fudgeDegrees
        
        r = self.radixChartGraphicsItem.\
            getRadiusForWheelNumber(self.wheelNumber + 1)
        planetTextRadius = r - ((r - self.drawPointRadius) / 3.0)
        
        textX = -1.0 * math.cos(math.radians(rotationDegrees)) * \
                planetTextRadius
        textY = 1.0 * math.sin(math.radians(rotationDegrees)) * \
                planetTextRadius
        rotationTransform.translate(textX, textY)
        rotationTransform.rotate(-1.0 * (self.degree + 90))

        rotatedTextPath = QPainterPath()
        rotatedTextPath.addPath(rotationTransform.map(textPath))

        painter.drawPath(rotatedTextPath)


        # Draw the text for the degrees of the sign the planet is in.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)

        # Normalize degree value.
        degreesInSign = self.degree
        while degreesInSign < 0:
            degreesInSign += 360.0
        while degreesInSign >= 360.0:
            degreesInSign -= 360.0

        # Get integer values of degrees and minutes.
        minutesInDegree = \
            int((degreesInSign - math.floor(degreesInSign)) * 60.0)
        degreesInSign = int(math.floor(degreesInSign))

        # Text.
        text = "{}\u00b0{}'".format(degreesInSign, minutesInDegree)
        
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        
        rotationTransform = QTransform()
        fudgeDegrees = 1.0
        rotationDegrees = self.degree + fudgeDegrees
        
        r = self.radixChartGraphicsItem.\
            getRadiusForWheelNumber(self.wheelNumber + 1)
        planetTextRadius = r - (2.0 * (r - self.drawPointRadius) / 3.0)
        
        textX = -1.0 * math.cos(math.radians(rotationDegrees)) * \
                planetTextRadius
        textY = 1.0 * math.sin(math.radians(rotationDegrees)) * \
                planetTextRadius
        rotationTransform.translate(textX, textY)
        rotationTransform.rotate(-1.0 * (self.degree + 90))

        rotatedTextPath = QPainterPath()
        rotatedTextPath.addPath(rotationTransform.map(textPath))

        painter.drawPath(rotatedTextPath)

        # Uncomment the below few lines of code to paint the boundingRect().
        # This is here just for future testing purposes.
        #painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
        #painter.setBrush(Qt.NoBrush)
        #painter.drawRect(self.boundingRect())
        
        # Restore the old paintbrush and pen.
        painter.setBrush(oldBrush)
        painter.setPen(oldPen)
        
class DeclinationChartGraphicsItem(QGraphicsItem):
    """QGraphicsItem that paints a chart for displaying various
    planets' declination.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger("astrologychart.PlanetDeclinationGraphicsItem")

        self.rulerWidth = 40.0
        self.rulerHeight = 600.0

        # These are on the verical axis.  Ruler height must be evenly
        # divisible by these tick size numbers below.
        self.bigTickSize = 50.0
        self.smallTickSize = 10.0

        # Value used in getXLocationForPlanetGroupNumber().
        self.planetLineLength = self.rulerWidth
        
    def getXLocationForPlanetGroupNumber(self, planetGroupNumber):
        """Returns the X location away from the origin for
        the location that the child items should draw their planets'
        QGraphicsItems.

        Arguments:
        planetGroupNumber - int value which is an index representing
                            the set of planets that having their
                            declination charted.  This index
                            value is 0-based, so 0 is the first set
                            of planets drawn to the right of the ruler.

        Returns:
        float - Width for where to start drawing the text for a planet.
        """

        x = self.planetLineLength + \
            (planetGroupNumber) * (2.0 * self.planetLineLength)
        
        return x

    
    def convertYValueToDegree(self, y):
        """Converts a tick Y value to it's equivalent in degrees.

        Arguments:
        y - float value for the Y coordinate value.

        Returns
        float - value for the degrees that this Y value represents..
        """

        # Our algorithm for conversion is to drop an order of magnitude.
        return (y / -10.0)
        
    def convertDegreeToYValue(self, degree):
        """Converts a degree value it's equivalent Y value in coordinates.

        Arguments:
        degree - float value for the degree the planet is at.

        Returns
        float - value for the Y coordinate location for the given degree.
        """

        # Our algorithm for conversion is the following.
        return degree * -10.0
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) is the location where the zero-tick
        # intersects the right side of the ruler.  The painting should
        # be relative to this point as the center.

        x = -1.0 * self.rulerWidth
        y = -1.0 * self.rulerHeight / 2.0
        rectF = QRectF(x, y, self.rulerWidth, self.rulerHeight)

        return rectF
    
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem. """

        # Coordinate (0, 0) is the location where the zero-tick
        # intersects the right side of the ruler.  The painting should
        # be relative to this point as the center.

        # Change the brush and pen in the painter.
        # We will restore it when done.
        oldBrush = painter.brush()
        oldPen = painter.pen()
        pen = painter.pen()
        pen.setColor(QColor(Qt.black))
        pen.setWidthF(0.0)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(QColor(Qt.black))
        painter.setBrush(brush)

        # Draw the rectangle for the ruler.
        rectF = self.boundingRect()
        painter.drawRect(rectF)

        # Now that the rectangle is drawn.  Everything can have a
        # solid pattern for its brush because we don't paint anything
        # else we don't want filled in.
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        
        # Draw small ticks.
        start = int(-1.0 * self.rulerHeight / 2.0)
        stop = int(self.rulerHeight / 2.0)
        step = int(self.smallTickSize)
        smallTickWidth = self.rulerWidth / 6.0
        for tick in range(start, stop, step):
            # Draw the tick line.
            x1 = -1.0 * smallTickWidth
            y1 = -1.0 * tick
            x2 = 0
            y2 = -1.0 * tick
            painter.drawLine(x1, y1, x2, y2)

        # Draw big ticks
        start = int(-1.0 * self.rulerHeight / 2.0)
        stop = int(self.rulerHeight / 2.0)
        step = int(self.bigTickSize)
        bigTickWidth = self.rulerWidth / 3.0
        for tick in range(start, stop, step):
            # Draw the tick line.
            x1 = -1.0 * bigTickWidth
            y1 = -1.0 * tick
            x2 = -1.0 * smallTickWidth
            y2 = -1.0 * tick
            painter.drawLine(x1, y1, x2, y2)

            # Draw the text for the ticks.
            font = QFont()
            font.setFamily("Lucida Console")
            font.setPointSize(10)
            
            x1 = -1.0 * self.rulerWidth
            y1 = -1.0 * tick
            converted = math.floor(-1 * self.convertYValueToDegree(float(tick)))
            text = "{}\u00b0".format(converted)
            textPath = QPainterPath()
            textPath.addText(0, 0, font, text)
            
            transform = QTransform()
            transform.translate(x1, y1)
            
            translatedPath = QPainterPath()
            translatedPath.addPath(transform.map(textPath))
            
            painter.drawPath(translatedPath)
            
        # Restore old paintbrush and pen.
        painter.setBrush(oldBrush)
        painter.setPen(oldPen)
    
class PlanetDeclinationGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is a 'planet' to be drawn with a
    DeclinationChartGraphicsItem object as its parent QGraphicsItem.
    """

    def __init__(self,
                 planetGlyphUnicode,
                 planetGlyphFontSize,
                 planetAbbreviation,
                 planetForegroundColor,
                 planetBackgroundColor,
                 degree = 0.0,
                 velocity = 0.0,
                 planetGroupNumber = 0,
                 parent=None,
                 scene=None):
        """Initializes the object with the given arguments.

        Arguments:
        planetGlyphUnicode - str holding the planet glyph.
        planetGlyphUnicode - float font size for drawing the glyph.
        planetAbbreviation - str holding the planet abbreviation.
        planetForegroundColor - QColor object for the foreground color to
                                be used for the drawing of the planet.
        planetBackgroundColor - QColor object for the background color to
                                be used for the drawing of the planet.
        degree - float value for the latitude degree location for where this
                 planet will be drawn.  If the value is not
                 in the range [-180.0, 180), it will be normalized so that it
                 is in that range before drawing.
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        planetGroupNumber - int value for the group of planets that this
                            planet belongs to.  This is so planets of
                            the same group (timestamp) can be drawn together.
                            The first group is at number 0.
        parent - DeclinationChartGraphicsItem that is the parent for this
                 QGraphicsItem.
        scene - QGraphicsScene object to draw this QGraphicsItem on.
        """
    
        # Logger
        self.log = \
            logging.getLogger("astrologychart.PlanetDeclinationGraphicsItem")

        super().__init__(parent, scene)

        # Save the parameter values.
        self.planetGlyphUnicode = planetGlyphUnicode
        self.planetGlyphFontSize = planetGlyphFontSize
        self.planetAbbreviation = planetAbbreviation
        self.planetForegroundColor = planetForegroundColor
        self.planetBackgroundColor = planetBackgroundColor
        self.degree = degree
        self.velocity = velocity
        self.planetGroupNumber = planetGroupNumber
        self.parentChartGraphicsItem = parent

        # Location where the line ends and the text begins.  This
        # value is obtained from the parent
        # DeclinationChartGraphicsItem object.
        self.lineEndX = 0.0

        # Call our overwritten self.setParentItem() manually so that
        # the parent object type can be verified.  This will also
        # subsequently have the (desired) side effect of
        # re-calculating self.lineEndX and updating the QGraphicsItem.
        self.setParentItem(parent)

        
    def setParentItem(self, parent):
        """Overwrites QGraphicsItem.setParentItem().  Needed so we can
        save off the parent in self.parentChartGraphicsItem.

        Arguments:
        parent -  DeclinationChartGraphicsItem parent object.
        """

        # Verify parent class.
        if parent != None and \
               not isinstance(parent, DeclinationChartGraphicsItem):
            
            raise TypeError("Argument 'parent' is not of type " + \
                            "'DeclinationChartGraphicsItem'")
        
        # Save off the parent.
        self.parentChartGraphicsItem = parent

        # Call self.setPlanetGroupNumber() again so the drawn points
        # can be recalculated.
        self.setPlanetGroupNumber(self.planetGroupNumber)
        
    def setDegree(self, degree):
        """Sets the location of the planet in degrees of the zodiac.

        Arguments:
        
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        """

        self.degree = degree
        self.update()
        
    def getDegree(self):
        """Returns the location of the planet in degrees of the zodiac.

        Returns:
        float - Value representing the degree location of the planet.
                The value returned will be between: [0.0, 360).
        """

        return self.degree

    def setVelocity(self, velocity):
        """Sets the velocity of the planet, in degrees per day.

        Arguments:
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.velocity = velocity
        self.update()

    def getVelocity(self):
        """Returns the velocity of the planet, in degrees per day.

        Returns:
        float - Value for the velocity of the planet, in degrees
                per day.
        """

        return self.velocity

    def setDegreeAndVelocity(self, degree, velocity):
        """Sets the degree location of the planet and the velocity of
        the planet, all at once.

        Arguments:
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.degree = degree
        self.velocity = velocity

        self.update()
        
    def setPlanetGroupNumber(self, planetGroupNumber):
        """Sets the planet group number that this QGraphicsItem is
        associated with.  The first group is number 0.
        
        Arguments:
        planetGroupNumber - int value for the group of planets that this
                            planet belongs to.  This is so planets of
                            the same group (timestamp) can be drawn together.
                            The first group is at number 0.
        """

        self.planetGroupNumber = planetGroupNumber


        # Update the self.lineEndX location point if we have a parent
        # chart set.
        if self.parentChartGraphicsItem != None:

            lineEndX = \
                self.parentChartGraphicsItem.\
                getXLocationForPlanetGroupNumber(self.planetGroupNumber)

            # Update variable only if the new value is different.
            if self.lineEndX != lineEndX:
                self.lineEndX = lineEndX
                self.update()

    def getPlanetGroupNumber(self):
        """Returns the planet group number that this planet is drawn
        on.  This value represents which group of planets that the
        planet is associated with when drawn on teh chart.  The first
        planet group is number 0.

        Returns:

        int - Value representing which planet group number the planet
              is drawn on.  A value of 0 indicates the first group on
              the right of the ruler.
        """

        return self.planetGroupNumber

    def getPlanetGlyphUnicode(self):
        """Returns the planet glyph in unicode."""

        return self.planetGlyphUnicode

    def getPlanetGlyphFontSize(self):
        """Returns the planet glyph font size."""

        return self.planetGlyphFontSize

    def getPlanetAbbreviation(self):
        """Returns the planet abbreviation."""

        return self.planetAbbreviation

    def getPlanetForegroundColor(self):
        """Returns the planet foreground color as a QColor object."""

        return self.planetForegroundColor

    def getPlanetBackgroundColor(self):
        """Returns the planet background color as a QColor object."""

        return self.planetBackgroundColor

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem.

        We implement this function by taking all the pieces, and doing
        an logical OR on the areas covered by their rectangles.  The
        rectangles are calculated in the same way that paint() is
        done.  Changes to paint() will required changes to this
        method.
        """

        # QRectF for the line.
        x1 = 0.0
        y1 = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        x2 = self.lineEndX
        y2 = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        lineRect = QRectF(QPointF(x1, y1), QPointF(x2, y2)).normalized()

        # QRectF for text of the planet glyph and degree.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)
        text = self.planetGlyphUnicode
        text += " {}\u00b0".format(self.degree)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        textX = self.lineEndX
        textY = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        transform.translate(textX, textY)
        transformedTextPath = QPainterPath()
        transformedTextPath.addPath(transform.map(textPath))
        textRect = transformedTextPath.boundingRect()

        # Unite all rectangles.
        rv = lineRect.united(textRect)
        
        return rv

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.
        
        The painting is done in three parts:
        - Paint the line from ruler to the location where the text starts.
        - Paint the text for the planet glyph and the degree it is at.

        Note: boundingRect() utilizes the same calculations as here,
        so if this function changes, then boundingRect() will need to
        be updated as well.
        """

        # Change the brush and pen in the painter.
        # We will restore it when done.
        oldBrush = painter.brush()
        oldPen = painter.pen()
        pen = painter.pen()
        pen.setColor(QColor(self.planetForegroundColor))
        pen.setWidthF(0.0)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(self.planetForegroundColor)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw the line.
        x1 = 0.0
        y1 = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        x2 = self.lineEndX
        y2 = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        painter.drawLine(x1, y1, x2, y2)

        # Draw the text for the planet.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)

        text = self.planetGlyphUnicode
        text += " {}\u00b0".format(self.degree)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        
        transform = QTransform()
        textX = self.lineEndX
        textY = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        transform.translate(textX, textY)
        transformedTextPath = QPainterPath()
        transformedTextPath.addPath(transform.map(textPath))
        painter.drawPath(transformedTextPath)

        # Uncomment the below few lines of code to paint the boundingRect().
        # This is here just for future testing purposes.
        #painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
        #painter.setBrush(Qt.NoBrush)
        #painter.drawRect(self.boundingRect())
        
        # Restore the old paintbrush and pen.
        painter.setBrush(oldBrush)
        painter.setPen(oldPen)
        
def testSiderealRadixChartGraphicsItem():
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
    
    item = SiderealRadixChartGraphicsItem()
    
    scene.addItem(item)

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()
    
def testRadixPlanetGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")
    
    from settings import SettingsKeys
    
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
    
    chartItem = SiderealRadixChartGraphicsItem()
    
    scene.addItem(chartItem)

    jupiter = \
        RadixPlanetGraphicsItem(SettingsKeys.planetJupiterGlyphUnicodeDefValue,
                                SettingsKeys.planetJupiterGlyphFontSizeDefValue,
                                SettingsKeys.planetJupiterAbbreviationDefValue,
                                SettingsKeys.planetJupiterForegroundColorDefValue,
                                SettingsKeys.planetJupiterBackgroundColorDefValue,
                                degree=5.0,
                                velocity=4.0,
                                wheelNumber=1,
                                parent=chartItem)
    venus = \
        RadixPlanetGraphicsItem(SettingsKeys.planetVenusGlyphUnicodeDefValue,
                                SettingsKeys.planetVenusGlyphFontSizeDefValue,
                                SettingsKeys.planetVenusAbbreviationDefValue,
                                QColor(Qt.red),
                                SettingsKeys.planetVenusBackgroundColorDefValue,
                                degree=9.0,
                                velocity=-2.0,
                                wheelNumber=0,
                                parent=chartItem)
    

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()


def testDeclinationChartGraphicsItem():
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
    
    chartItem = DeclinationChartGraphicsItem()
    
    scene.addItem(chartItem)

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()

def testPlanetDeclinationGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")
    
    from settings import SettingsKeys
    
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
    
    chartItem = DeclinationChartGraphicsItem()
    scene.addItem(chartItem)

    moon = \
        PlanetDeclinationGraphicsItem(
        SettingsKeys.planetMoonGlyphUnicodeDefValue,
        SettingsKeys.planetMoonGlyphFontSizeDefValue,
        SettingsKeys.planetMoonAbbreviationDefValue,
        QColor(Qt.blue),
        SettingsKeys.planetMoonBackgroundColorDefValue,
        degree=17.56,
        velocity=2.0,
        planetGroupNumber=0,
        parent=chartItem)
    
    mercury = \
        PlanetDeclinationGraphicsItem(
        SettingsKeys.planetMercuryGlyphUnicodeDefValue,
        SettingsKeys.planetMercuryGlyphFontSizeDefValue,
        SettingsKeys.planetMercuryAbbreviationDefValue,
        QColor(Qt.green),
        SettingsKeys.planetMercuryBackgroundColorDefValue,
        degree=5.2,
        velocity=-2.0,
        planetGroupNumber=0,
        parent=chartItem)

    jupiter = \
        PlanetDeclinationGraphicsItem(
        SettingsKeys.planetJupiterGlyphUnicodeDefValue,
        SettingsKeys.planetJupiterGlyphFontSizeDefValue,
        SettingsKeys.planetJupiterAbbreviationDefValue,
        QColor(Qt.red),
        SettingsKeys.planetJupiterBackgroundColorDefValue,
        degree=-8.0,
        velocity=3.0,
        planetGroupNumber=0,
        parent=chartItem)

    moon = \
        PlanetDeclinationGraphicsItem(
        SettingsKeys.planetMoonGlyphUnicodeDefValue,
        SettingsKeys.planetMoonGlyphFontSizeDefValue,
        SettingsKeys.planetMoonAbbreviationDefValue,
        QColor(Qt.blue),
        SettingsKeys.planetMoonBackgroundColorDefValue,
        degree=5,
        velocity=2.0,
        planetGroupNumber=1,
        parent=chartItem)
    
    mercury = \
        PlanetDeclinationGraphicsItem(
        SettingsKeys.planetMercuryGlyphUnicodeDefValue,
        SettingsKeys.planetMercuryGlyphFontSizeDefValue,
        SettingsKeys.planetMercuryAbbreviationDefValue,
        QColor(Qt.green),
        SettingsKeys.planetMercuryBackgroundColorDefValue,
        degree=-9.2,
        velocity=-2.0,
        planetGroupNumber=1,
        parent=chartItem)

    jupiter = \
        PlanetDeclinationGraphicsItem(
        SettingsKeys.planetJupiterGlyphUnicodeDefValue,
        SettingsKeys.planetJupiterGlyphFontSizeDefValue,
        SettingsKeys.planetJupiterAbbreviationDefValue,
        QColor(Qt.red),
        SettingsKeys.planetJupiterBackgroundColorDefValue,
        degree=7.0,
        velocity=3.0,
        planetGroupNumber=1,
        parent=chartItem)
    
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
    #testSiderealRadixChartGraphicsItem()
    #testRadixPlanetGraphicsItem()
    #testDeclinationChartGraphicsItem()
    testPlanetDeclinationGraphicsItem()
    
    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()
    #app.exec_()
    

        
