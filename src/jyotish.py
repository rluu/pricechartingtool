
class Drishti:
    
    def __init__(self, planetName, drishti, strengthRatio):
        """Initalizes the Drishti information with the given parameters.

        Parametres are as follows:

        planetName - str holding the graha name.

        drishti    - int holding the bhava aspect relative to the graha.
                     This value is the count, inclusive.
                     This value must be in the range [1, 12].
                     For example:
                       1 is the same bhava as the graha.
                       7 is the bhava opposite the graha.

        strengthRatio - float holding strength of the aspect.
                     This value must bein the range [0.0, 1.0].
                     For example:
                         1.0  is 100 percent strength.
                         0.5  is  50 percent strength.
                         0.25 is  25 percent strength.
        """

        # Validate inputs.
        if planetName is None \
                or planetName == "" \
                or not isinstance(planetName, str):
            raise RuntimeError("planetName must be a non-empty str.")

        if drishti is None or not isinsteance(drishti, int):
            raise RuntimeError("drishti must be an int.")
        elif drishti < 1 or drishti > 12:
            raise RuntimeError("drishti must be in the range [1, 12].")

        if strengthRatio is None or not isinsteance(strengthRatio, float):
            raise RuntimeError("strengthRatio must be a float.")
        elif strengthRatio < 0.0 or strengthRatio > 1.0:
            raise RuntimeError("strengthRatio must be in the range [0.0, 1.0].")

        # Store values.
        self.planetName = planetName
        self.drishti = drishti
        self.strengthRatio = strengthRatio

    def getDrishtiAngle(self):
        """Converts the drishti to an angle in the range [0.0, 360.0).
        """

        angle = (drishti - 1) * 30.0

        if angle < 0.0 or angle >= 360.0:
            raise RuntimeError("Validation failed on converting a " + \
                "drishti to an angle in degrees.  " + \
                "drishti: {}".format(drishti) + \
                ", angle: {}".format(angle))

        return angle

    def __str__(self):
        """Returns a string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns a string representation of this object."""

        formatStr = "[planetName={}, drishti={}, strengthRatio={}]"

        returnStr = formatStr.format(self.planetName,
                                     self.drishti,
                                     self.strengthRatio)

        return returnStr



class ParasaraDrishtis:

    parasaraDrishtis = []

    # TODO_rluu: Make sure all the values are correct per Parasara.
    parasaraDrishtis.append(Drishti("Sun", 1, 1.0))
    parasaraDrishtis.append(Drishti("Sun", 7, 1.0))
    parasaraDrishtis.append(Drishti("Sun", 4, 0.75))
    parasaraDrishtis.append(Drishti("Sun", 8, 0.75))
    parasaraDrishtis.append(Drishti("Sun", 5, 0.5))
    parasaraDrishtis.append(Drishti("Sun", 9, 0.5))
    parasaraDrishtis.append(Drishti("Sun", 3, 0.25))
    parasaraDrishtis.append(Drishti("Sun", 10, 0.25))

    parasaraDrishtis.append(Drishti("Moon", 1, 1.0))
    parasaraDrishtis.append(Drishti("Moon", 7, 1.0))
    parasaraDrishtis.append(Drishti("Moon", 4, 0.75))
    parasaraDrishtis.append(Drishti("Moon", 8, 0.75))
    parasaraDrishtis.append(Drishti("Moon", 5, 0.5))
    parasaraDrishtis.append(Drishti("Moon", 9, 0.5))
    parasaraDrishtis.append(Drishti("Moon", 3, 0.25))
    parasaraDrishtis.append(Drishti("Moon", 10, 0.25))

    parasaraDrishtis.append(Drishti("Mercury", 1, 1.0))
    parasaraDrishtis.append(Drishti("Mercury", 7, 1.0))
    parasaraDrishtis.append(Drishti("Mercury", 4, 0.75))
    parasaraDrishtis.append(Drishti("Mercury", 8, 0.75))
    parasaraDrishtis.append(Drishti("Mercury", 5, 0.5))
    parasaraDrishtis.append(Drishti("Mercury", 9, 0.5))
    parasaraDrishtis.append(Drishti("Mercury", 3, 0.25))
    parasaraDrishtis.append(Drishti("Mercury", 10, 0.25))

    parasaraDrishtis.append(Drishti("Venus", 1, 1.0))
    parasaraDrishtis.append(Drishti("Venus", 7, 1.0))
    parasaraDrishtis.append(Drishti("Venus", 4, 0.75))
    parasaraDrishtis.append(Drishti("Venus", 8, 0.75))
    parasaraDrishtis.append(Drishti("Venus", 5, 0.5))
    parasaraDrishtis.append(Drishti("Venus", 9, 0.5))
    parasaraDrishtis.append(Drishti("Venus", 3, 0.25))
    parasaraDrishtis.append(Drishti("Venus", 10, 0.25))

    parasaraDrishtis.append(Drishti("Mars", 1, 1.0))
    parasaraDrishtis.append(Drishti("Mars", 7, 1.0))
    parasaraDrishtis.append(Drishti("Mars", 4, 0.75))
    parasaraDrishtis.append(Drishti("Mars", 8, 0.75))
    parasaraDrishtis.append(Drishti("Mars", 5, 0.5))
    parasaraDrishtis.append(Drishti("Mars", 9, 0.5))
    parasaraDrishtis.append(Drishti("Mars", 3, 0.25))
    parasaraDrishtis.append(Drishti("Mars", 10, 0.25))

    parasaraDrishtis.append(Drishti("Jupiter", 1, 1.0))
    parasaraDrishtis.append(Drishti("Jupiter", 7, 1.0))
    parasaraDrishtis.append(Drishti("Jupiter", 4, 0.75))
    parasaraDrishtis.append(Drishti("Jupiter", 8, 0.75))
    parasaraDrishtis.append(Drishti("Jupiter", 5, 0.5))
    parasaraDrishtis.append(Drishti("Jupiter", 9, 0.5))
    parasaraDrishtis.append(Drishti("Jupiter", 3, 0.25))
    parasaraDrishtis.append(Drishti("Jupiter", 10, 0.25))

    parasaraDrishtis.append(Drishti("Saturn", 1, 1.0))
    parasaraDrishtis.append(Drishti("Saturn", 7, 1.0))
    parasaraDrishtis.append(Drishti("Saturn", 4, 0.75))
    parasaraDrishtis.append(Drishti("Saturn", 8, 0.75))
    parasaraDrishtis.append(Drishti("Saturn", 5, 0.5))
    parasaraDrishtis.append(Drishti("Saturn", 9, 0.5))
    parasaraDrishtis.append(Drishti("Saturn", 3, 0.25))
    parasaraDrishtis.append(Drishti("Saturn", 10, 0.25))

    parasaraDrishtis.append(Drishti("TrueNorthNode", 1, 1.0))
    parasaraDrishtis.append(Drishti("TrueNorthNode", 7, 1.0))
    parasaraDrishtis.append(Drishti("TrueNorthNode", 4, 0.75))
    parasaraDrishtis.append(Drishti("TrueNorthNode", 8, 0.75))
    parasaraDrishtis.append(Drishti("TrueNorthNode", 5, 0.5))
    parasaraDrishtis.append(Drishti("TrueNorthNode", 9, 0.5))
    parasaraDrishtis.append(Drishti("TrueNorthNode", 3, 0.25))
    parasaraDrishtis.append(Drishti("TrueNorthNode", 10, 0.25))

    parasaraDrishtis.append(Drishti("TrueSouthNode", 1, 1.0))
    parasaraDrishtis.append(Drishti("TrueSouthNode", 7, 1.0))
    parasaraDrishtis.append(Drishti("TrueSouthNode", 4, 0.75))
    parasaraDrishtis.append(Drishti("TrueSouthNode", 8, 0.75))
    parasaraDrishtis.append(Drishti("TrueSouthNode", 5, 0.5))
    parasaraDrishtis.append(Drishti("TrueSouthNode", 9, 0.5))
    parasaraDrishtis.append(Drishti("TrueSouthNode", 3, 0.25))
    parasaraDrishtis.append(Drishti("TrueSouthNode", 10, 0.25))


class Jyotish:
    """Class containing Jyotish-related methods and information."""

    def getFullStrengthAspectDegreesForPlanetName(planetName, includeZeroDegrees=False):
        aspectDegrees = []

        drishtis = []
        for drishti in ParasaraDrishtis.parasarDrishtis:
            if drishti.planetName == planetName:
                if includeZeroDegrees == False and drishti.getDrishtiAngle() == 0.0:
                    continue
                else:
                    if drishti.strengthRatio == 1.0:
                        drishtis.append(drishti)

        for drishti in drishtis:
            aspectDegrees.append(drishti.getDrishtiAngle())

        return aspectDegrees


