
# For PyQt widgets.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Color():
    """Class containing static class variables of customized QColors that
    are easier to access/reference than creating them myself at every
    location I use them."""

    # Black and White colors.
    white = QColor(Qt.white)
    black = QColor(Qt.black)

    # Gray colors.
    gray = QColor(Qt.gray)                  # (160, 160, 160) / #A0A0A0
    darkGray = QColor(Qt.darkGray)          # (128, 128, 128) / #808080
    veryDarkGray = QColor(96, 96, 96)
    veryVeryDarkGray = QColor(64, 64, 64)
    almostBlack = QColor(32, 32, 32)
    lightGray = QColor(Qt.lightGray)        # (192, 192, 192) / #C0C0C0
    veryLightGray = QColor(224, 224, 224)

    # Red colors.
    red = QColor(Qt.red)                    # (255,   0,   0) / #FF0000
    darkRed = QColor(Qt.darkRed)            # (128,   0,   0) / #800000
    lightRed = QColor(255, 51, 51)
    veryLightRed = QColor(255, 102, 102)

    # Green colors.
    green = QColor(0, 153, 0)
    limeGreen = QColor(0, 255, 0)
    darkGreen = QColor(0, 102, 0)
    veryDarkGreen = QColor(0, 51, 0)
    lightGreen = QColor(51, 255, 51)
    veryLightGreen = QColor(102, 255, 102)
    neonGreen = QColor(0, 255, 0)
    oliveGreen = QColor(128, 128, 0)
    lightPineGreen = QColor(51, 102, 0)
    darkPineGreen = QColor(25, 51, 0)

    # Blue colors.
    blue = QColor(Qt.blue)                  # (  0,   0, 255) / #0000FF
    darkBlue = QColor(Qt.darkBlue)          # (  0,   0, 128) / #000080
    lightBlue = QColor(0, 102, 204)
    darkBabyBlue = QColor(0, 128, 255)
    lightBabyBlue = QColor(51, 153, 255)

    # Blue-green-ish colors.
    turquoise = QColor(0, 204, 204)
    teal = QColor(0, 153, 153)
    cyan = QColor(Qt.cyan)                  # (  0, 255, 255) / #00FFFF
    darkCyan = QColor(Qt.darkCyan)          # (  0, 128, 128) / #008080

    # Purple colors.
    purple = QColor(127, 0, 255)
    darkPurple = QColor(76, 0, 153)
    lightPurple = QColor(153, 51, 255)
    veryLightPurple = QColor(178, 102, 255)

    # Pink colors.
    magenta = QColor(Qt.magenta)            # (255,   0, 255) / #FF00FF
    darkMagenta = QColor(Qt.darkMagenta)    # (128,   0, 128) / #800080
    hotPink = QColor(255, 0, 127)
    darkHotPink = QColor(204, 0, 102)
    pink = QColor(255, 51, 255)
    darkPink = QColor(204, 0, 204)
    lightPink = QColor(255, 102, 255)
    veryLightPink = QColor(255, 153, 255)

    # Yellow colors.
    yellow = QColor(Qt.yellow)
    darkYellow = QColor(204, 204, 0)        # Looks like a dirty yellow.
    veryDarkYellow = QColor(153, 153, 0)    # Looks like a dirty dark yellow.
    lightYellow = QColor(255, 255, 102)

    # Orange colors.
    orange = QColor(255, 128, 0)
    darkOrange = QColor(204, 102, 0)
    veryDarkOrange = QColor(153, 76, 0)
    lightOrange = QColor(255, 153, 51)
    veryLightOrange = QColor(255, 178, 102)

    # TODO_rluu: Add brown.

