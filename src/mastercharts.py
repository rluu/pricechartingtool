
# For logging.
import logging

# For calculating square roots and other calculations.
import math


class MasterCharts:
    """Class for making calculations based on the Gann Master Charts
    (Square of 9, etc.)
    """


    @staticmethod
    def getSqOf9CycleAndAngle(value, base=1):
        """Returns a tuple holding the cycle number and angle in
        degrees (in the square of 9 chart) for a given float value.

        Arguments:
        value - float value for the number to look up.
        base  - int value for the base number that is in the
                center of the square of 9.
        """

        # TODO:  write this function.
        pass

    @staticmethod
    def getSqOf9Cycle(value, base=1):
        """Returns an int holding the cycle number (in the square of 9
        chart) that the float value resides in.

        Arguments:
        value - float value for the number to look up.
        base  - int value for the base number that is in the
                center of the square of 9.

        Returns:
        int value for the cycle that the float value falls in.
        """

        # TODO:  write this function.
        pass

    @staticmethod
    def getSqOf9Angle(value, base=1):
        """Returns the angle (in the square of 9 chart) that the given float
        value resides at.

        Arguments:
        value - float value for the number to look up.
        base  - int value for the base number that is in the
                center of the square of 9.

        Returns:
        float value for the angle that the float value falls at.
        """
        
        # TODO:  write this function.
        pass

    @staticmethod
    def getSqOf9ImportantAngles(angleDeg):
        """Returns the important square of 9 angles relative to the
        given angle.  These are basically normalized values for
        angleDeg plus the following degree values:

        0
        22.5
        45
        67.5
        90
        112.5
        135
        157.5
        180
        202.5
        225
        247.5
        270
        292.5
        315
        337.5
        
        Arguments:
        angleDeg - float value that is the angle of interest on the
                   square of 9 chart.

        Returns:
        list of float values holding the angle degrees on the square of 9
        that are important relative to the given input angle.
        """
        
        # TODO:  write this function.
        pass

    def getSqOf9Value(angleDeg, cycle, base=1):
        """Returns the square of 9 value at the given angle and cycle number.

        Arguments:
        angleDeg - float value for the angle on the square of 9.
        cycle    - int value for the numerical cycle on the square of 9.
                   This value must be positive.
        base     - int value for the base number that is in the
                   center of the square of 9.
                   
        Returns:
        float value for the number at the given angle and cycle on the
        square of 9.
        """

        # TODO:  write this function.
        pass

    def getSqOf9Values(angleDeg, minValue, maxValue, base=1):
        """Returns a list of numbers on the square of 9 at a given angle.
        
        Arguments:
        angleDeg - float value for the angle on the square of 9.
        minValue - float value for the minimum value (lower limit) to
                   include in returned list.
        maxValue - float value for the maximum value (lower limit) to
                   include in returned list.
        base     - int value for the base number that is in the
                   center of the square of 9.

        Returns:
        list of float values for the numbers at the given angle.
        """

        # TODO:  write this function.
        pass

