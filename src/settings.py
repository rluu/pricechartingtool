


from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor


class SettingsKeys():
    """Static class that holds keys that are used in the QSettings storage."""

    
    # QSettings key for the defaultPriceBarDataOpenDirectory.
    defaultPriceBarDataOpenDirectorySettingsKey = \
        "ui/defaultPriceBarDataOpenDirectory"

    # QSettings key for zoomScaleFactor (float).
    zoomScaleFactorSettingsKey = \
        "ui/pricebarchart/zoomScaleFactor"

    # QSettings default value for zoomScaleFactor (float).
    zoomScaleFactorSettingsDefValue = 1.2
    
    # QSettings key for the higherPriceBarColor (QColor object).
    higherPriceBarColorSettingsKey = \
        "ui/pricebarchart/higherPriceBarColor"

    # QSettings default value for the higherPriceBarColor (QColor object).
    higherPriceBarColorSettingsDefValue = QColor(Qt.green)

    # QSettings key for the lowerPriceBarColor (QColor object).
    lowerPriceBarColorSettingsKey = \
        "ui/pricebarchart/lowerPriceBarColor"

    # QSettings default value for the lowerPriceBarColor (QColor object).
    lowerPriceBarColorSettingsDefValue = QColor(Qt.red)



    # QSettings key for the planet glyph unicode of the Ascendant.
    planetAscendantGlyphUnicodeKey = \
        "ui/astrology/ascendantGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Ascendant.
    planetAscendantGlyphUnicodeDefValue = "As"

    # QSettings key for the planet glyph font size of the Ascendant.
    planetAscendantGlyphFontSizeKey = \
        "ui/astrology/ascendantGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Ascendant.
    planetAscendantGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Ascendant.
    planetAscendantAbbreviationKey = \
        "ui/astrology/ascendantAbbreviation"

    # QSettings default value for the planet abbreviation of the Ascendant.
    planetAscendantAbbreviationDefValue = "As"

    # QSettings key for the foreground color of the Ascendant.
    planetAscendantForegroundColorKey = \
        "ui/astrology/ascendantForegroundColor"

    # QSettings default value for the foreground color of the Ascendant.
    planetAscendantForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Ascendant.
    planetAscendantBackgroundColorKey = \
        "ui/astrology/ascendantBackgroundColor"

    # QSettings default value for the background color of the Ascendant.
    planetAscendantBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Midheaven.
    planetMidheavenGlyphUnicodeKey = \
        "ui/astrology/midheavenGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Midheaven.
    planetMidheavenGlyphUnicodeDefValue = "MC"

    # QSettings key for the planet glyph font size of the Midheaven.
    planetMidheavenGlyphFontSizeKey = \
        "ui/astrology/midheavenGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Midheaven.
    planetMidheavenGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Midheaven.
    planetMidheavenAbbreviationKey = \
        "ui/astrology/midheavenAbbreviation"

    # QSettings default value for the planet abbreviation of the Midheaven.
    planetMidheavenAbbreviationDefValue = "MC"

    # QSettings key for the foreground color of the Midheaven.
    planetMidheavenForegroundColorKey = \
        "ui/astrology/midheavenForegroundColor"

    # QSettings default value for the foreground color of the Midheaven.
    planetMidheavenForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Midheaven.
    planetMidheavenBackgroundColorKey = \
        "ui/astrology/midheavenBackgroundColor"

    # QSettings default value for the background color of the Midheaven.
    planetMidheavenBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Sun.
    planetSunGlyphUnicodeKey = \
        "ui/astrology/sunGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Sun.
    planetSunGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Sun.
    planetSunGlyphFontSizeKey = \
        "ui/astrology/sunGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Sun.
    planetSunGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Sun.
    planetSunAbbreviationKey = \
        "ui/astrology/sunAbbreviation"

    # QSettings default value for the planet abbreviation of the Sun.
    planetSunAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Sun.
    planetSunForegroundColorKey = \
        "ui/astrology/sunForegroundColor"

    # QSettings default value for the foreground color of the Sun.
    planetSunForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Sun.
    planetSunBackgroundColorKey = \
        "ui/astrology/sunBackgroundColor"

    # QSettings default value for the background color of the Sun.
    planetSunBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Moon.
    planetMoonGlyphUnicodeKey = \
        "ui/astrology/moonGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Moon.
    planetMoonGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Moon.
    planetMoonGlyphFontSizeKey = \
        "ui/astrology/moonGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Moon.
    planetMoonGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Moon.
    planetMoonAbbreviationKey = \
        "ui/astrology/moonAbbreviation"

    # QSettings default value for the planet abbreviation of the Moon.
    planetMoonAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Moon.
    planetMoonForegroundColorKey = \
        "ui/astrology/moonForegroundColor"

    # QSettings default value for the foreground color of the Moon.
    planetMoonForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Moon.
    planetMoonBackgroundColorKey = \
        "ui/astrology/moonBackgroundColor"

    # QSettings default value for the background color of the Moon.
    planetMoonBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Mercury.
    planetMercuryGlyphUnicodeKey = \
        "ui/astrology/mercuryGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mercury.
    planetMercuryGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Mercury.
    planetMercuryGlyphFontSizeKey = \
        "ui/astrology/mercuryGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mercury.
    planetMercuryGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mercury.
    planetMercuryAbbreviationKey = \
        "ui/astrology/mercuryAbbreviation"

    # QSettings default value for the planet abbreviation of the Mercury.
    planetMercuryAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Mercury.
    planetMercuryForegroundColorKey = \
        "ui/astrology/mercuryForegroundColor"

    # QSettings default value for the foreground color of the Mercury.
    planetMercuryForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mercury.
    planetMercuryBackgroundColorKey = \
        "ui/astrology/mercuryBackgroundColor"

    # QSettings default value for the background color of the Mercury.
    planetMercuryBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Venus.
    planetVenusGlyphUnicodeKey = \
        "ui/astrology/venusGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Venus.
    planetVenusGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Venus.
    planetVenusGlyphFontSizeKey = \
        "ui/astrology/venusGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Venus.
    planetVenusGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Venus.
    planetVenusAbbreviationKey = \
        "ui/astrology/venusAbbreviation"

    # QSettings default value for the planet abbreviation of the Venus.
    planetVenusAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Venus.
    planetVenusForegroundColorKey = \
        "ui/astrology/venusForegroundColor"

    # QSettings default value for the foreground color of the Venus.
    planetVenusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Venus.
    planetVenusBackgroundColorKey = \
        "ui/astrology/venusBackgroundColor"

    # QSettings default value for the background color of the Venus.
    planetVenusBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Mars.
    planetMarsGlyphUnicodeKey = \
        "ui/astrology/marsGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mars.
    planetMarsGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Mars.
    planetMarsGlyphFontSizeKey = \
        "ui/astrology/marsGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mars.
    planetMarsGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mars.
    planetMarsAbbreviationKey = \
        "ui/astrology/marsAbbreviation"

    # QSettings default value for the planet abbreviation of the Mars.
    planetMarsAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Mars.
    planetMarsForegroundColorKey = \
        "ui/astrology/marsForegroundColor"

    # QSettings default value for the foreground color of the Mars.
    planetMarsForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mars.
    planetMarsBackgroundColorKey = \
        "ui/astrology/marsBackgroundColor"

    # QSettings default value for the background color of the Mars.
    planetMarsBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Jupiter.
    planetJupiterGlyphUnicodeKey = \
        "ui/astrology/jupiterGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Jupiter.
    planetJupiterGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Jupiter.
    planetJupiterGlyphFontSizeKey = \
        "ui/astrology/jupiterGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Jupiter.
    planetJupiterGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Jupiter.
    planetJupiterAbbreviationKey = \
        "ui/astrology/jupiterAbbreviation"

    # QSettings default value for the planet abbreviation of the Jupiter.
    planetJupiterAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Jupiter.
    planetJupiterForegroundColorKey = \
        "ui/astrology/jupiterForegroundColor"

    # QSettings default value for the foreground color of the Jupiter.
    planetJupiterForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Jupiter.
    planetJupiterBackgroundColorKey = \
        "ui/astrology/jupiterBackgroundColor"

    # QSettings default value for the background color of the Jupiter.
    planetJupiterBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Saturn.
    planetSaturnGlyphUnicodeKey = \
        "ui/astrology/saturnGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Saturn.
    planetSaturnGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Saturn.
    planetSaturnGlyphFontSizeKey = \
        "ui/astrology/saturnGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Saturn.
    planetSaturnGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Saturn.
    planetSaturnAbbreviationKey = \
        "ui/astrology/saturnAbbreviation"

    # QSettings default value for the planet abbreviation of the Saturn.
    planetSaturnAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Saturn.
    planetSaturnForegroundColorKey = \
        "ui/astrology/saturnForegroundColor"

    # QSettings default value for the foreground color of the Saturn.
    planetSaturnForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Saturn.
    planetSaturnBackgroundColorKey = \
        "ui/astrology/saturnBackgroundColor"

    # QSettings default value for the background color of the Saturn.
    planetSaturnBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Uranus.
    planetUranusGlyphUnicodeKey = \
        "ui/astrology/uranusGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Uranus.
    planetUranusGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Uranus.
    planetUranusGlyphFontSizeKey = \
        "ui/astrology/uranusGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Uranus.
    planetUranusGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Uranus.
    planetUranusAbbreviationKey = \
        "ui/astrology/uranusAbbreviation"

    # QSettings default value for the planet abbreviation of the Uranus.
    planetUranusAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Uranus.
    planetUranusForegroundColorKey = \
        "ui/astrology/uranusForegroundColor"

    # QSettings default value for the foreground color of the Uranus.
    planetUranusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Uranus.
    planetUranusBackgroundColorKey = \
        "ui/astrology/uranusBackgroundColor"

    # QSettings default value for the background color of the Uranus.
    planetUranusBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Neptune.
    planetNeptuneGlyphUnicodeKey = \
        "ui/astrology/neptuneGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Neptune.
    planetNeptuneGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Neptune.
    planetNeptuneGlyphFontSizeKey = \
        "ui/astrology/neptuneGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Neptune.
    planetNeptuneGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Neptune.
    planetNeptuneAbbreviationKey = \
        "ui/astrology/neptuneAbbreviation"

    # QSettings default value for the planet abbreviation of the Neptune.
    planetNeptuneAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Neptune.
    planetNeptuneForegroundColorKey = \
        "ui/astrology/neptuneForegroundColor"

    # QSettings default value for the foreground color of the Neptune.
    planetNeptuneForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Neptune.
    planetNeptuneBackgroundColorKey = \
        "ui/astrology/neptuneBackgroundColor"

    # QSettings default value for the background color of the Neptune.
    planetNeptuneBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Pluto.
    planetPlutoGlyphUnicodeKey = \
        "ui/astrology/plutoGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Pluto.
    planetPlutoGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Pluto.
    planetPlutoGlyphFontSizeKey = \
        "ui/astrology/plutoGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Pluto.
    planetPlutoGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Pluto.
    planetPlutoAbbreviationKey = \
        "ui/astrology/plutoAbbreviation"

    # QSettings default value for the planet abbreviation of the Pluto.
    planetPlutoAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Pluto.
    planetPlutoForegroundColorKey = \
        "ui/astrology/plutoForegroundColor"

    # QSettings default value for the foreground color of the Pluto.
    planetPlutoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pluto.
    planetPlutoBackgroundColorKey = \
        "ui/astrology/plutoBackgroundColor"

    # QSettings default value for the background color of the Pluto.
    planetPlutoBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the MeanNorthNode.
    planetMeanNorthNodeGlyphUnicodeKey = \
        "ui/astrology/meanNorthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanNorthNode.
    planetMeanNorthNodeGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the MeanNorthNode.
    planetMeanNorthNodeGlyphFontSizeKey = \
        "ui/astrology/meanNorthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanNorthNode.
    planetMeanNorthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanNorthNode.
    planetMeanNorthNodeAbbreviationKey = \
        "ui/astrology/meanNorthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanNorthNode.
    planetMeanNorthNodeAbbreviationDefValue = ""

    # QSettings key for the foreground color of the MeanNorthNode.
    planetMeanNorthNodeForegroundColorKey = \
        "ui/astrology/meanNorthNodeForegroundColor"

    # QSettings default value for the foreground color of the MeanNorthNode.
    planetMeanNorthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanNorthNode.
    planetMeanNorthNodeBackgroundColorKey = \
        "ui/astrology/meanNorthNodeBackgroundColor"

    # QSettings default value for the background color of the MeanNorthNode.
    planetMeanNorthNodeBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the MeanSouthNode.
    planetMeanSouthNodeGlyphUnicodeKey = \
        "ui/astrology/meanSouthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanSouthNode.
    planetMeanSouthNodeGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the MeanSouthNode.
    planetMeanSouthNodeGlyphFontSizeKey = \
        "ui/astrology/meanSouthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanSouthNode.
    planetMeanSouthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanSouthNode.
    planetMeanSouthNodeAbbreviationKey = \
        "ui/astrology/meanSouthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanSouthNode.
    planetMeanSouthNodeAbbreviationDefValue = ""

    # QSettings key for the foreground color of the MeanSouthNode.
    planetMeanSouthNodeForegroundColorKey = \
        "ui/astrology/meanSouthNodeForegroundColor"

    # QSettings default value for the foreground color of the MeanSouthNode.
    planetMeanSouthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanSouthNode.
    planetMeanSouthNodeBackgroundColorKey = \
        "ui/astrology/meanSouthNodeBackgroundColor"

    # QSettings default value for the background color of the MeanSouthNode.
    planetMeanSouthNodeBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the TrueNorthNode.
    planetTrueNorthNodeGlyphUnicodeKey = \
        "ui/astrology/trueNorthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the TrueNorthNode.
    planetTrueNorthNodeGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the TrueNorthNode.
    planetTrueNorthNodeGlyphFontSizeKey = \
        "ui/astrology/trueNorthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the TrueNorthNode.
    planetTrueNorthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the TrueNorthNode.
    planetTrueNorthNodeAbbreviationKey = \
        "ui/astrology/trueNorthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the TrueNorthNode.
    planetTrueNorthNodeAbbreviationDefValue = ""

    # QSettings key for the foreground color of the TrueNorthNode.
    planetTrueNorthNodeForegroundColorKey = \
        "ui/astrology/trueNorthNodeForegroundColor"

    # QSettings default value for the foreground color of the TrueNorthNode.
    planetTrueNorthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the TrueNorthNode.
    planetTrueNorthNodeBackgroundColorKey = \
        "ui/astrology/trueNorthNodeBackgroundColor"

    # QSettings default value for the background color of the TrueNorthNode.
    planetTrueNorthNodeBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the TrueSouthNode.
    planetTrueSouthNodeGlyphUnicodeKey = \
        "ui/astrology/trueSouthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the TrueSouthNode.
    planetTrueSouthNodeGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the TrueSouthNode.
    planetTrueSouthNodeGlyphFontSizeKey = \
        "ui/astrology/trueSouthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the TrueSouthNode.
    planetTrueSouthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the TrueSouthNode.
    planetTrueSouthNodeAbbreviationKey = \
        "ui/astrology/trueSouthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the TrueSouthNode.
    planetTrueSouthNodeAbbreviationDefValue = ""

    # QSettings key for the foreground color of the TrueSouthNode.
    planetTrueSouthNodeForegroundColorKey = \
        "ui/astrology/trueSouthNodeForegroundColor"

    # QSettings default value for the foreground color of the TrueSouthNode.
    planetTrueSouthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the TrueSouthNode.
    planetTrueSouthNodeBackgroundColorKey = \
        "ui/astrology/trueSouthNodeBackgroundColor"

    # QSettings default value for the background color of the TrueSouthNode.
    planetTrueSouthNodeBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/meanLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/meanLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanLunarApogee.
    planetMeanLunarApogeeAbbreviationKey = \
        "ui/astrology/meanLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanLunarApogee.
    planetMeanLunarApogeeAbbreviationDefValue = ""

    # QSettings key for the foreground color of the MeanLunarApogee.
    planetMeanLunarApogeeForegroundColorKey = \
        "ui/astrology/meanLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the MeanLunarApogee.
    planetMeanLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanLunarApogee.
    planetMeanLunarApogeeBackgroundColorKey = \
        "ui/astrology/meanLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the MeanLunarApogee.
    planetMeanLunarApogeeBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/osculatingLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/osculatingLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeAbbreviationKey = \
        "ui/astrology/osculatingLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeAbbreviationDefValue = ""

    # QSettings key for the foreground color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeForegroundColorKey = \
        "ui/astrology/osculatingLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeBackgroundColorKey = \
        "ui/astrology/osculatingLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/interpolatedLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/interpolatedLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeAbbreviationKey = \
        "ui/astrology/interpolatedLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeAbbreviationDefValue = ""

    # QSettings key for the foreground color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeForegroundColorKey = \
        "ui/astrology/interpolatedLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeBackgroundColorKey = \
        "ui/astrology/interpolatedLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphUnicodeKey = \
        "ui/astrology/interpolatedLunarPerigeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphFontSizeKey = \
        "ui/astrology/interpolatedLunarPerigeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeAbbreviationKey = \
        "ui/astrology/interpolatedLunarPerigeeAbbreviation"

    # QSettings default value for the planet abbreviation of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeAbbreviationDefValue = ""

    # QSettings key for the foreground color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeForegroundColorKey = \
        "ui/astrology/interpolatedLunarPerigeeForegroundColor"

    # QSettings default value for the foreground color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeBackgroundColorKey = \
        "ui/astrology/interpolatedLunarPerigeeBackgroundColor"

    # QSettings default value for the background color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Earth.
    planetEarthGlyphUnicodeKey = \
        "ui/astrology/earthGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Earth.
    planetEarthGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Earth.
    planetEarthGlyphFontSizeKey = \
        "ui/astrology/earthGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Earth.
    planetEarthGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Earth.
    planetEarthAbbreviationKey = \
        "ui/astrology/earthAbbreviation"

    # QSettings default value for the planet abbreviation of the Earth.
    planetEarthAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Earth.
    planetEarthForegroundColorKey = \
        "ui/astrology/earthForegroundColor"

    # QSettings default value for the foreground color of the Earth.
    planetEarthForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Earth.
    planetEarthBackgroundColorKey = \
        "ui/astrology/earthBackgroundColor"

    # QSettings default value for the background color of the Earth.
    planetEarthBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Chiron.
    planetChironGlyphUnicodeKey = \
        "ui/astrology/chironGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Chiron.
    planetChironGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Chiron.
    planetChironGlyphFontSizeKey = \
        "ui/astrology/chironGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Chiron.
    planetChironGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Chiron.
    planetChironAbbreviationKey = \
        "ui/astrology/chironAbbreviation"

    # QSettings default value for the planet abbreviation of the Chiron.
    planetChironAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Chiron.
    planetChironForegroundColorKey = \
        "ui/astrology/chironForegroundColor"

    # QSettings default value for the foreground color of the Chiron.
    planetChironForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Chiron.
    planetChironBackgroundColorKey = \
        "ui/astrology/chironBackgroundColor"

    # QSettings default value for the background color of the Chiron.
    planetChironBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Gulika.
    planetGulikaGlyphUnicodeKey = \
        "ui/astrology/gulikaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Gulika.
    planetGulikaGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Gulika.
    planetGulikaGlyphFontSizeKey = \
        "ui/astrology/gulikaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Gulika.
    planetGulikaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Gulika.
    planetGulikaAbbreviationKey = \
        "ui/astrology/gulikaAbbreviation"

    # QSettings default value for the planet abbreviation of the Gulika.
    planetGulikaAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Gulika.
    planetGulikaForegroundColorKey = \
        "ui/astrology/gulikaForegroundColor"

    # QSettings default value for the foreground color of the Gulika.
    planetGulikaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Gulika.
    planetGulikaBackgroundColorKey = \
        "ui/astrology/gulikaBackgroundColor"

    # QSettings default value for the background color of the Gulika.
    planetGulikaBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the Mandi.
    planetMandiGlyphUnicodeKey = \
        "ui/astrology/mandiGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mandi.
    planetMandiGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the Mandi.
    planetMandiGlyphFontSizeKey = \
        "ui/astrology/mandiGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mandi.
    planetMandiGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mandi.
    planetMandiAbbreviationKey = \
        "ui/astrology/mandiAbbreviation"

    # QSettings default value for the planet abbreviation of the Mandi.
    planetMandiAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Mandi.
    planetMandiForegroundColorKey = \
        "ui/astrology/mandiForegroundColor"

    # QSettings default value for the foreground color of the Mandi.
    planetMandiForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mandi.
    planetMandiBackgroundColorKey = \
        "ui/astrology/mandiBackgroundColor"

    # QSettings default value for the background color of the Mandi.
    planetMandiBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the HoraLagna.
    planetHoraLagnaGlyphUnicodeKey = \
        "ui/astrology/horaLagnaGlyphUnicode"

    # QSettings key for the planet glyph font size of the HoraLagna.
    planetHoraLagnaGlyphFontSizeKey = \
        "ui/astrology/horaLagnaGlyphFontSize"

    # QSettings key for the planet abbreviation of the HoraLagna.
    planetHoraLagnaAbbreviationKey = \
        "ui/astrology/horaLagnaAbbreviation"

    # QSettings key for the foreground color of the HoraLagna.
    planetHoraLagnaForegroundColorKey = \
        "ui/astrology/horaLagnaForegroundColor"

    # QSettings key for the background color of the HoraLagna.
    planetHoraLagnaBackgroundColorKey = \
        "ui/astrology/horaLagnaBackgroundColor"



    # QSettings key for the planet glyph unicode of the GhatiLagna.
    planetGhatiLagnaGlyphUnicodeKey = \
        "ui/astrology/ghatiLagnaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the GhatiLagna.
    planetGhatiLagnaGlyphUnicodeDefValue = ""

    # QSettings key for the planet glyph font size of the GhatiLagna.
    planetGhatiLagnaGlyphFontSizeKey = \
        "ui/astrology/ghatiLagnaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the GhatiLagna.
    planetGhatiLagnaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the GhatiLagna.
    planetGhatiLagnaAbbreviationKey = \
        "ui/astrology/ghatiLagnaAbbreviation"

    # QSettings default value for the planet abbreviation of the GhatiLagna.
    planetGhatiLagnaAbbreviationDefValue = ""

    # QSettings key for the foreground color of the GhatiLagna.
    planetGhatiLagnaForegroundColorKey = \
        "ui/astrology/ghatiLagnaForegroundColor"

    # QSettings default value for the foreground color of the GhatiLagna.
    planetGhatiLagnaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the GhatiLagna.
    planetGhatiLagnaBackgroundColorKey = \
        "ui/astrology/ghatiLagnaBackgroundColor"

    # QSettings default value for the background color of the GhatiLagna.
    planetGhatiLagnaBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Aries.
    signAriesGlyphUnicodeKey = \
        "ui/astrology/ariesGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Aries.
    signAriesGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Aries.
    signAriesGlyphFontSizeKey = \
        "ui/astrology/ariesGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Aries.
    signAriesGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Aries.
    signAriesAbbreviationKey = \
        "ui/astrology/ariesAbbreviation"

    # QSettings default value for the sign abbreviation of the Aries.
    signAriesAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Aries.
    signAriesForegroundColorKey = \
        "ui/astrology/ariesForegroundColor"

    # QSettings default value for the foreground color of the Aries.
    signAriesForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Aries.
    signAriesBackgroundColorKey = \
        "ui/astrology/ariesBackgroundColor"

    # QSettings default value for the background color of the Aries.
    signAriesBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Taurus.
    signTaurusGlyphUnicodeKey = \
        "ui/astrology/taurusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Taurus.
    signTaurusGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Taurus.
    signTaurusGlyphFontSizeKey = \
        "ui/astrology/taurusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Taurus.
    signTaurusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Taurus.
    signTaurusAbbreviationKey = \
        "ui/astrology/taurusAbbreviation"

    # QSettings default value for the sign abbreviation of the Taurus.
    signTaurusAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Taurus.
    signTaurusForegroundColorKey = \
        "ui/astrology/taurusForegroundColor"

    # QSettings default value for the foreground color of the Taurus.
    signTaurusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Taurus.
    signTaurusBackgroundColorKey = \
        "ui/astrology/taurusBackgroundColor"

    # QSettings default value for the background color of the Taurus.
    signTaurusBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Gemini.
    signGeminiGlyphUnicodeKey = \
        "ui/astrology/geminiGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Gemini.
    signGeminiGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Gemini.
    signGeminiGlyphFontSizeKey = \
        "ui/astrology/geminiGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Gemini.
    signGeminiGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Gemini.
    signGeminiAbbreviationKey = \
        "ui/astrology/geminiAbbreviation"

    # QSettings default value for the sign abbreviation of the Gemini.
    signGeminiAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Gemini.
    signGeminiForegroundColorKey = \
        "ui/astrology/geminiForegroundColor"

    # QSettings default value for the foreground color of the Gemini.
    signGeminiForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Gemini.
    signGeminiBackgroundColorKey = \
        "ui/astrology/geminiBackgroundColor"

    # QSettings default value for the background color of the Gemini.
    signGeminiBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Cancer.
    signCancerGlyphUnicodeKey = \
        "ui/astrology/cancerGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Cancer.
    signCancerGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Cancer.
    signCancerGlyphFontSizeKey = \
        "ui/astrology/cancerGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Cancer.
    signCancerGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Cancer.
    signCancerAbbreviationKey = \
        "ui/astrology/cancerAbbreviation"

    # QSettings default value for the sign abbreviation of the Cancer.
    signCancerAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Cancer.
    signCancerForegroundColorKey = \
        "ui/astrology/cancerForegroundColor"

    # QSettings default value for the foreground color of the Cancer.
    signCancerForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Cancer.
    signCancerBackgroundColorKey = \
        "ui/astrology/cancerBackgroundColor"

    # QSettings default value for the background color of the Cancer.
    signCancerBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Leo.
    signLeoGlyphUnicodeKey = \
        "ui/astrology/leoGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Leo.
    signLeoGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Leo.
    signLeoGlyphFontSizeKey = \
        "ui/astrology/leoGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Leo.
    signLeoGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Leo.
    signLeoAbbreviationKey = \
        "ui/astrology/leoAbbreviation"

    # QSettings default value for the sign abbreviation of the Leo.
    signLeoAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Leo.
    signLeoForegroundColorKey = \
        "ui/astrology/leoForegroundColor"

    # QSettings default value for the foreground color of the Leo.
    signLeoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Leo.
    signLeoBackgroundColorKey = \
        "ui/astrology/leoBackgroundColor"

    # QSettings default value for the background color of the Leo.
    signLeoBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Virgo.
    signVirgoGlyphUnicodeKey = \
        "ui/astrology/virgoGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Virgo.
    signVirgoGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Virgo.
    signVirgoGlyphFontSizeKey = \
        "ui/astrology/virgoGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Virgo.
    signVirgoGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Virgo.
    signVirgoAbbreviationKey = \
        "ui/astrology/virgoAbbreviation"

    # QSettings default value for the sign abbreviation of the Virgo.
    signVirgoAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Virgo.
    signVirgoForegroundColorKey = \
        "ui/astrology/virgoForegroundColor"

    # QSettings default value for the foreground color of the Virgo.
    signVirgoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Virgo.
    signVirgoBackgroundColorKey = \
        "ui/astrology/virgoBackgroundColor"

    # QSettings default value for the background color of the Virgo.
    signVirgoBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Libra.
    signLibraGlyphUnicodeKey = \
        "ui/astrology/libraGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Libra.
    signLibraGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Libra.
    signLibraGlyphFontSizeKey = \
        "ui/astrology/libraGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Libra.
    signLibraGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Libra.
    signLibraAbbreviationKey = \
        "ui/astrology/libraAbbreviation"

    # QSettings default value for the sign abbreviation of the Libra.
    signLibraAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Libra.
    signLibraForegroundColorKey = \
        "ui/astrology/libraForegroundColor"

    # QSettings default value for the foreground color of the Libra.
    signLibraForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Libra.
    signLibraBackgroundColorKey = \
        "ui/astrology/libraBackgroundColor"

    # QSettings default value for the background color of the Libra.
    signLibraBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Scorpio.
    signScorpioGlyphUnicodeKey = \
        "ui/astrology/scorpioGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Scorpio.
    signScorpioGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Scorpio.
    signScorpioGlyphFontSizeKey = \
        "ui/astrology/scorpioGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Scorpio.
    signScorpioGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Scorpio.
    signScorpioAbbreviationKey = \
        "ui/astrology/scorpioAbbreviation"

    # QSettings default value for the sign abbreviation of the Scorpio.
    signScorpioAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Scorpio.
    signScorpioForegroundColorKey = \
        "ui/astrology/scorpioForegroundColor"

    # QSettings default value for the foreground color of the Scorpio.
    signScorpioForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Scorpio.
    signScorpioBackgroundColorKey = \
        "ui/astrology/scorpioBackgroundColor"

    # QSettings default value for the background color of the Scorpio.
    signScorpioBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Sagittarius.
    signSagittariusGlyphUnicodeKey = \
        "ui/astrology/sagittariusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Sagittarius.
    signSagittariusGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Sagittarius.
    signSagittariusGlyphFontSizeKey = \
        "ui/astrology/sagittariusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Sagittarius.
    signSagittariusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Sagittarius.
    signSagittariusAbbreviationKey = \
        "ui/astrology/sagittariusAbbreviation"

    # QSettings default value for the sign abbreviation of the Sagittarius.
    signSagittariusAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Sagittarius.
    signSagittariusForegroundColorKey = \
        "ui/astrology/sagittariusForegroundColor"

    # QSettings default value for the foreground color of the Sagittarius.
    signSagittariusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Sagittarius.
    signSagittariusBackgroundColorKey = \
        "ui/astrology/sagittariusBackgroundColor"

    # QSettings default value for the background color of the Sagittarius.
    signSagittariusBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Capricorn.
    signCapricornGlyphUnicodeKey = \
        "ui/astrology/capricornGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Capricorn.
    signCapricornGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Capricorn.
    signCapricornGlyphFontSizeKey = \
        "ui/astrology/capricornGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Capricorn.
    signCapricornGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Capricorn.
    signCapricornAbbreviationKey = \
        "ui/astrology/capricornAbbreviation"

    # QSettings default value for the sign abbreviation of the Capricorn.
    signCapricornAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Capricorn.
    signCapricornForegroundColorKey = \
        "ui/astrology/capricornForegroundColor"

    # QSettings default value for the foreground color of the Capricorn.
    signCapricornForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Capricorn.
    signCapricornBackgroundColorKey = \
        "ui/astrology/capricornBackgroundColor"

    # QSettings default value for the background color of the Capricorn.
    signCapricornBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Aquarius.
    signAquariusGlyphUnicodeKey = \
        "ui/astrology/aquariusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Aquarius.
    signAquariusGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Aquarius.
    signAquariusGlyphFontSizeKey = \
        "ui/astrology/aquariusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Aquarius.
    signAquariusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Aquarius.
    signAquariusAbbreviationKey = \
        "ui/astrology/aquariusAbbreviation"

    # QSettings default value for the sign abbreviation of the Aquarius.
    signAquariusAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Aquarius.
    signAquariusForegroundColorKey = \
        "ui/astrology/aquariusForegroundColor"

    # QSettings default value for the foreground color of the Aquarius.
    signAquariusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Aquarius.
    signAquariusBackgroundColorKey = \
        "ui/astrology/aquariusBackgroundColor"

    # QSettings default value for the background color of the Aquarius.
    signAquariusBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the sign glyph unicode of the Pisces.
    signPiscesGlyphUnicodeKey = \
        "ui/astrology/piscesGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Pisces.
    signPiscesGlyphUnicodeDefValue = ""

    # QSettings key for the sign glyph font size of the Pisces.
    signPiscesGlyphFontSizeKey = \
        "ui/astrology/piscesGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Pisces.
    signPiscesGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Pisces.
    signPiscesAbbreviationKey = \
        "ui/astrology/piscesAbbreviation"

    # QSettings default value for the sign abbreviation of the Pisces.
    signPiscesAbbreviationDefValue = ""

    # QSettings key for the foreground color of the Pisces.
    signPiscesForegroundColorKey = \
        "ui/astrology/piscesForegroundColor"

    # QSettings default value for the foreground color of the Pisces.
    signPiscesForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pisces.
    signPiscesBackgroundColorKey = \
        "ui/astrology/piscesBackgroundColor"

    # QSettings default value for the background color of the Pisces.
    signPiscesBackgroundColorDefValue = QColor(Qt.white)



