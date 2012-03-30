


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
    higherPriceBarColorSettingsDefValue = QColor(0, 128, 0, 255)

    # QSettings key for the lowerPriceBarColor (QColor object).
    lowerPriceBarColorSettingsKey = \
        "ui/pricebarchart/lowerPriceBarColor"

    # QSettings default value for the lowerPriceBarColor (QColor object).
    lowerPriceBarColorSettingsDefValue = QColor(128, 0, 0, 255)

    # QSettings key for the BarCountGraphicsItem color (QColor object).
    barCountGraphicsItemColorSettingsKey = \
        "ui/pricebarchart/barCountGraphicsItemColor"

    # QSettings default value for the BarCountGraphicsItem color (QColor object).
    barCountGraphicsItemColorSettingsDefValue = QColor(Qt.black)

    # QSettings key for the BarCountGraphicsItem text color (QColor object).
    barCountGraphicsItemTextColorSettingsKey = \
        "ui/pricebarchart/barCountGraphicsItemTextColor"

    # QSettings default value for the BarCountGraphicsItem text color (QColor object).
    barCountGraphicsItemTextColorSettingsDefValue = QColor(Qt.black)

    # QSettings key for the ModalScaleGraphicsItem color (QColor object).
    modalScaleGraphicsItemColorSettingsKey = \
        "ui/pricebarchart/modalScaleGraphicsItemColor"

    # QSettings default value for the ModalScaleGraphicsItem color (QColor object).
    modalScaleGraphicsItemColorSettingsDefValue = QColor(Qt.black)

    # QSettings key for the ModalScaleGraphicsItem text color (QColor object).
    modalScaleGraphicsItemTextColorSettingsKey = \
        "ui/pricebarchart/modalScaleGraphicsItemTextColor"

    # QSettings default value for the ModalScaleGraphicsItem text color (QColor object).
    modalScaleGraphicsItemTextColorSettingsDefValue = QColor(Qt.black)


    # QSettings key for the planet glyph unicode of the Retrograde.
    planetRetrogradeGlyphUnicodeKey = \
        "ui/astrology/retrogradeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Retrograde.
    planetRetrogradeGlyphUnicodeDefValue = "\u211e"

    # QSettings key for the planet glyph font size of the Retrograde.
    planetRetrogradeGlyphFontSizeKey = \
        "ui/astrology/retrogradeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Retrograde.
    planetRetrogradeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Retrograde.
    planetRetrogradeAbbreviationKey = \
        "ui/astrology/retrogradeAbbreviation"

    # QSettings default value for the planet abbreviation of the Retrograde.
    planetRetrogradeAbbreviationDefValue = "Rx"

    # QSettings key for the foreground color of the Retrograde.
    planetRetrogradeForegroundColorKey = \
        "ui/astrology/retrogradeForegroundColor"

    # QSettings default value for the foreground color of the Retrograde.
    planetRetrogradeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Retrograde.
    planetRetrogradeBackgroundColorKey = \
        "ui/astrology/retrogradeBackgroundColor"

    # QSettings default value for the background color of the Retrograde.
    planetRetrogradeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H1.
    planetH1GlyphUnicodeKey = \
        "ui/astrology/h1GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H1.
    planetH1GlyphUnicodeDefValue = "As"

    # QSettings key for the planet glyph font size of the H1.
    planetH1GlyphFontSizeKey = \
        "ui/astrology/h1GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H1.
    planetH1GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H1.
    planetH1AbbreviationKey = \
        "ui/astrology/h1Abbreviation"

    # QSettings default value for the planet abbreviation of the H1.
    planetH1AbbreviationDefValue = "As"

    # QSettings key for the foreground color of the H1.
    planetH1ForegroundColorKey = \
        "ui/astrology/h1ForegroundColor"

    # QSettings default value for the foreground color of the H1.
    planetH1ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H1.
    planetH1BackgroundColorKey = \
        "ui/astrology/h1BackgroundColor"

    # QSettings default value for the background color of the H1.
    planetH1BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H2.
    planetH2GlyphUnicodeKey = \
        "ui/astrology/h2GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H2.
    planetH2GlyphUnicodeDefValue = "H2"

    # QSettings key for the planet glyph font size of the H2.
    planetH2GlyphFontSizeKey = \
        "ui/astrology/h2GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H2.
    planetH2GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H2.
    planetH2AbbreviationKey = \
        "ui/astrology/h2Abbreviation"

    # QSettings default value for the planet abbreviation of the H2.
    planetH2AbbreviationDefValue = "H2"

    # QSettings key for the foreground color of the H2.
    planetH2ForegroundColorKey = \
        "ui/astrology/h2ForegroundColor"

    # QSettings default value for the foreground color of the H2.
    planetH2ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H2.
    planetH2BackgroundColorKey = \
        "ui/astrology/h2BackgroundColor"

    # QSettings default value for the background color of the H2.
    planetH2BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H3.
    planetH3GlyphUnicodeKey = \
        "ui/astrology/h3GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H3.
    planetH3GlyphUnicodeDefValue = "H3"

    # QSettings key for the planet glyph font size of the H3.
    planetH3GlyphFontSizeKey = \
        "ui/astrology/h3GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H3.
    planetH3GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H3.
    planetH3AbbreviationKey = \
        "ui/astrology/h3Abbreviation"

    # QSettings default value for the planet abbreviation of the H3.
    planetH3AbbreviationDefValue = "H3"

    # QSettings key for the foreground color of the H3.
    planetH3ForegroundColorKey = \
        "ui/astrology/h3ForegroundColor"

    # QSettings default value for the foreground color of the H3.
    planetH3ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H3.
    planetH3BackgroundColorKey = \
        "ui/astrology/h3BackgroundColor"

    # QSettings default value for the background color of the H3.
    planetH3BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H4.
    planetH4GlyphUnicodeKey = \
        "ui/astrology/h4GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H4.
    planetH4GlyphUnicodeDefValue = "H4"

    # QSettings key for the planet glyph font size of the H4.
    planetH4GlyphFontSizeKey = \
        "ui/astrology/h4GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H4.
    planetH4GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H4.
    planetH4AbbreviationKey = \
        "ui/astrology/h4Abbreviation"

    # QSettings default value for the planet abbreviation of the H4.
    planetH4AbbreviationDefValue = "H4"

    # QSettings key for the foreground color of the H4.
    planetH4ForegroundColorKey = \
        "ui/astrology/h4ForegroundColor"

    # QSettings default value for the foreground color of the H4.
    planetH4ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H4.
    planetH4BackgroundColorKey = \
        "ui/astrology/h4BackgroundColor"

    # QSettings default value for the background color of the H4.
    planetH4BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H5.
    planetH5GlyphUnicodeKey = \
        "ui/astrology/h5GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H5.
    planetH5GlyphUnicodeDefValue = "H5"

    # QSettings key for the planet glyph font size of the H5.
    planetH5GlyphFontSizeKey = \
        "ui/astrology/h5GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H5.
    planetH5GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H5.
    planetH5AbbreviationKey = \
        "ui/astrology/h5Abbreviation"

    # QSettings default value for the planet abbreviation of the H5.
    planetH5AbbreviationDefValue = "H5"

    # QSettings key for the foreground color of the H5.
    planetH5ForegroundColorKey = \
        "ui/astrology/h5ForegroundColor"

    # QSettings default value for the foreground color of the H5.
    planetH5ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H5.
    planetH5BackgroundColorKey = \
        "ui/astrology/h5BackgroundColor"

    # QSettings default value for the background color of the H5.
    planetH5BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H6.
    planetH6GlyphUnicodeKey = \
        "ui/astrology/h6GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H6.
    planetH6GlyphUnicodeDefValue = "H6"

    # QSettings key for the planet glyph font size of the H6.
    planetH6GlyphFontSizeKey = \
        "ui/astrology/h6GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H6.
    planetH6GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H6.
    planetH6AbbreviationKey = \
        "ui/astrology/h6Abbreviation"

    # QSettings default value for the planet abbreviation of the H6.
    planetH6AbbreviationDefValue = "H6"

    # QSettings key for the foreground color of the H6.
    planetH6ForegroundColorKey = \
        "ui/astrology/h6ForegroundColor"

    # QSettings default value for the foreground color of the H6.
    planetH6ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H6.
    planetH6BackgroundColorKey = \
        "ui/astrology/h6BackgroundColor"

    # QSettings default value for the background color of the H6.
    planetH6BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H7.
    planetH7GlyphUnicodeKey = \
        "ui/astrology/h7GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H7.
    planetH7GlyphUnicodeDefValue = "H7"

    # QSettings key for the planet glyph font size of the H7.
    planetH7GlyphFontSizeKey = \
        "ui/astrology/h7GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H7.
    planetH7GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H7.
    planetH7AbbreviationKey = \
        "ui/astrology/h7Abbreviation"

    # QSettings default value for the planet abbreviation of the H7.
    planetH7AbbreviationDefValue = "H7"

    # QSettings key for the foreground color of the H7.
    planetH7ForegroundColorKey = \
        "ui/astrology/h7ForegroundColor"

    # QSettings default value for the foreground color of the H7.
    planetH7ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H7.
    planetH7BackgroundColorKey = \
        "ui/astrology/h7BackgroundColor"

    # QSettings default value for the background color of the H7.
    planetH7BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H8.
    planetH8GlyphUnicodeKey = \
        "ui/astrology/h8GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H8.
    planetH8GlyphUnicodeDefValue = "H8"

    # QSettings key for the planet glyph font size of the H8.
    planetH8GlyphFontSizeKey = \
        "ui/astrology/h8GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H8.
    planetH8GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H8.
    planetH8AbbreviationKey = \
        "ui/astrology/h8Abbreviation"

    # QSettings default value for the planet abbreviation of the H8.
    planetH8AbbreviationDefValue = "H8"

    # QSettings key for the foreground color of the H8.
    planetH8ForegroundColorKey = \
        "ui/astrology/h8ForegroundColor"

    # QSettings default value for the foreground color of the H8.
    planetH8ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H8.
    planetH8BackgroundColorKey = \
        "ui/astrology/h8BackgroundColor"

    # QSettings default value for the background color of the H8.
    planetH8BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H9.
    planetH9GlyphUnicodeKey = \
        "ui/astrology/h9GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H9.
    planetH9GlyphUnicodeDefValue = "H9"

    # QSettings key for the planet glyph font size of the H9.
    planetH9GlyphFontSizeKey = \
        "ui/astrology/h9GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H9.
    planetH9GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H9.
    planetH9AbbreviationKey = \
        "ui/astrology/h9Abbreviation"

    # QSettings default value for the planet abbreviation of the H9.
    planetH9AbbreviationDefValue = "H9"

    # QSettings key for the foreground color of the H9.
    planetH9ForegroundColorKey = \
        "ui/astrology/h9ForegroundColor"

    # QSettings default value for the foreground color of the H9.
    planetH9ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H9.
    planetH9BackgroundColorKey = \
        "ui/astrology/h9BackgroundColor"

    # QSettings default value for the background color of the H9.
    planetH9BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H10.
    planetH10GlyphUnicodeKey = \
        "ui/astrology/h10GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H10.
    planetH10GlyphUnicodeDefValue = "H10"

    # QSettings key for the planet glyph font size of the H10.
    planetH10GlyphFontSizeKey = \
        "ui/astrology/h10GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H10.
    planetH10GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H10.
    planetH10AbbreviationKey = \
        "ui/astrology/h10Abbreviation"

    # QSettings default value for the planet abbreviation of the H10.
    planetH10AbbreviationDefValue = "H10"

    # QSettings key for the foreground color of the H10.
    planetH10ForegroundColorKey = \
        "ui/astrology/h10ForegroundColor"

    # QSettings default value for the foreground color of the H10.
    planetH10ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H10.
    planetH10BackgroundColorKey = \
        "ui/astrology/h10BackgroundColor"

    # QSettings default value for the background color of the H10.
    planetH10BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H11.
    planetH11GlyphUnicodeKey = \
        "ui/astrology/h11GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H11.
    planetH11GlyphUnicodeDefValue = "H11"

    # QSettings key for the planet glyph font size of the H11.
    planetH11GlyphFontSizeKey = \
        "ui/astrology/h11GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H11.
    planetH11GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H11.
    planetH11AbbreviationKey = \
        "ui/astrology/h11Abbreviation"

    # QSettings default value for the planet abbreviation of the H11.
    planetH11AbbreviationDefValue = "H11"

    # QSettings key for the foreground color of the H11.
    planetH11ForegroundColorKey = \
        "ui/astrology/h11ForegroundColor"

    # QSettings default value for the foreground color of the H11.
    planetH11ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H11.
    planetH11BackgroundColorKey = \
        "ui/astrology/h11BackgroundColor"

    # QSettings default value for the background color of the H11.
    planetH11BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the H12.
    planetH12GlyphUnicodeKey = \
        "ui/astrology/h12GlyphUnicode"

    # QSettings default value for the planet glyph unicode of the H12.
    planetH12GlyphUnicodeDefValue = "H12"

    # QSettings key for the planet glyph font size of the H12.
    planetH12GlyphFontSizeKey = \
        "ui/astrology/h12GlyphFontSize"

    # QSettings default value for the planet glyph font size of the H12.
    planetH12GlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the H12.
    planetH12AbbreviationKey = \
        "ui/astrology/h12Abbreviation"

    # QSettings default value for the planet abbreviation of the H12.
    planetH12AbbreviationDefValue = "H12"

    # QSettings key for the foreground color of the H12.
    planetH12ForegroundColorKey = \
        "ui/astrology/h12ForegroundColor"

    # QSettings default value for the foreground color of the H12.
    planetH12ForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the H12.
    planetH12BackgroundColorKey = \
        "ui/astrology/h12BackgroundColor"

    # QSettings default value for the background color of the H12.
    planetH12BackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the HoraLagna.
    planetHoraLagnaGlyphUnicodeKey = \
        "ui/astrology/horaLagnaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the HoraLagna.
    planetHoraLagnaGlyphUnicodeDefValue = "HL"

    # QSettings key for the planet glyph font size of the HoraLagna.
    planetHoraLagnaGlyphFontSizeKey = \
        "ui/astrology/horaLagnaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the HoraLagna.
    planetHoraLagnaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the HoraLagna.
    planetHoraLagnaAbbreviationKey = \
        "ui/astrology/horaLagnaAbbreviation"

    # QSettings default value for the planet abbreviation of the HoraLagna.
    planetHoraLagnaAbbreviationDefValue = "HL"

    # QSettings key for the foreground color of the HoraLagna.
    planetHoraLagnaForegroundColorKey = \
        "ui/astrology/horaLagnaForegroundColor"

    # QSettings default value for the foreground color of the HoraLagna.
    planetHoraLagnaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the HoraLagna.
    planetHoraLagnaBackgroundColorKey = \
        "ui/astrology/horaLagnaBackgroundColor"

    # QSettings default value for the background color of the HoraLagna.
    planetHoraLagnaBackgroundColorDefValue = QColor(Qt.white)



    # QSettings key for the planet glyph unicode of the GhatiLagna.
    planetGhatiLagnaGlyphUnicodeKey = \
        "ui/astrology/ghatiLagnaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the GhatiLagna.
    planetGhatiLagnaGlyphUnicodeDefValue = "GL"

    # QSettings key for the planet glyph font size of the GhatiLagna.
    planetGhatiLagnaGlyphFontSizeKey = \
        "ui/astrology/ghatiLagnaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the GhatiLagna.
    planetGhatiLagnaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the GhatiLagna.
    planetGhatiLagnaAbbreviationKey = \
        "ui/astrology/ghatiLagnaAbbreviation"

    # QSettings default value for the planet abbreviation of the GhatiLagna.
    planetGhatiLagnaAbbreviationDefValue = "GL"

    # QSettings key for the foreground color of the GhatiLagna.
    planetGhatiLagnaForegroundColorKey = \
        "ui/astrology/ghatiLagnaForegroundColor"

    # QSettings default value for the foreground color of the GhatiLagna.
    planetGhatiLagnaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the GhatiLagna.
    planetGhatiLagnaBackgroundColorKey = \
        "ui/astrology/ghatiLagnaBackgroundColor"

    # QSettings default value for the background color of the GhatiLagna.
    planetGhatiLagnaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/meanLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphUnicodeDefValue = "MLA"

    # QSettings key for the planet glyph font size of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/meanLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanLunarApogee.
    planetMeanLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanLunarApogee.
    planetMeanLunarApogeeAbbreviationKey = \
        "ui/astrology/meanLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanLunarApogee.
    planetMeanLunarApogeeAbbreviationDefValue = "MLA"

    # QSettings key for the foreground color of the MeanLunarApogee.
    planetMeanLunarApogeeForegroundColorKey = \
        "ui/astrology/meanLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the MeanLunarApogee.
    planetMeanLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanLunarApogee.
    planetMeanLunarApogeeBackgroundColorKey = \
        "ui/astrology/meanLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the MeanLunarApogee.
    planetMeanLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/osculatingLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphUnicodeDefValue = "OLA"

    # QSettings key for the planet glyph font size of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/osculatingLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeAbbreviationKey = \
        "ui/astrology/osculatingLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeAbbreviationDefValue = "OLA"

    # QSettings key for the foreground color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeForegroundColorKey = \
        "ui/astrology/osculatingLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeBackgroundColorKey = \
        "ui/astrology/osculatingLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the OsculatingLunarApogee.
    planetOsculatingLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphUnicodeKey = \
        "ui/astrology/interpolatedLunarApogeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphUnicodeDefValue = "ILA"

    # QSettings key for the planet glyph font size of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphFontSizeKey = \
        "ui/astrology/interpolatedLunarApogeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeAbbreviationKey = \
        "ui/astrology/interpolatedLunarApogeeAbbreviation"

    # QSettings default value for the planet abbreviation of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeAbbreviationDefValue = "ILA"

    # QSettings key for the foreground color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeForegroundColorKey = \
        "ui/astrology/interpolatedLunarApogeeForegroundColor"

    # QSettings default value for the foreground color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeBackgroundColorKey = \
        "ui/astrology/interpolatedLunarApogeeBackgroundColor"

    # QSettings default value for the background color of the InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphUnicodeKey = \
        "ui/astrology/interpolatedLunarPerigeeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphUnicodeDefValue = "ILP"

    # QSettings key for the planet glyph font size of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphFontSizeKey = \
        "ui/astrology/interpolatedLunarPerigeeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeAbbreviationKey = \
        "ui/astrology/interpolatedLunarPerigeeAbbreviation"

    # QSettings default value for the planet abbreviation of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeAbbreviationDefValue = "ILP"

    # QSettings key for the foreground color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeForegroundColorKey = \
        "ui/astrology/interpolatedLunarPerigeeForegroundColor"

    # QSettings default value for the foreground color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeBackgroundColorKey = \
        "ui/astrology/interpolatedLunarPerigeeBackgroundColor"

    # QSettings default value for the background color of the InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Sun.
    planetSunGlyphUnicodeKey = \
        "ui/astrology/sunGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Sun.
    planetSunGlyphUnicodeDefValue = "\u2609"

    # QSettings key for the planet glyph font size of the Sun.
    planetSunGlyphFontSizeKey = \
        "ui/astrology/sunGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Sun.
    planetSunGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Sun.
    planetSunAbbreviationKey = \
        "ui/astrology/sunAbbreviation"

    # QSettings default value for the planet abbreviation of the Sun.
    planetSunAbbreviationDefValue = "Su"

    # QSettings key for the foreground color of the Sun.
    planetSunForegroundColorKey = \
        "ui/astrology/sunForegroundColor"

    # QSettings default value for the foreground color of the Sun.
    planetSunForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Sun.
    planetSunBackgroundColorKey = \
        "ui/astrology/sunBackgroundColor"

    # QSettings default value for the background color of the Sun.
    planetSunBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Moon.
    planetMoonGlyphUnicodeKey = \
        "ui/astrology/moonGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Moon.
    planetMoonGlyphUnicodeDefValue = "\u263d"

    # QSettings key for the planet glyph font size of the Moon.
    planetMoonGlyphFontSizeKey = \
        "ui/astrology/moonGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Moon.
    planetMoonGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Moon.
    planetMoonAbbreviationKey = \
        "ui/astrology/moonAbbreviation"

    # QSettings default value for the planet abbreviation of the Moon.
    planetMoonAbbreviationDefValue = "Mo"

    # QSettings key for the foreground color of the Moon.
    planetMoonForegroundColorKey = \
        "ui/astrology/moonForegroundColor"

    # QSettings default value for the foreground color of the Moon.
    planetMoonForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Moon.
    planetMoonBackgroundColorKey = \
        "ui/astrology/moonBackgroundColor"

    # QSettings default value for the background color of the Moon.
    planetMoonBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mercury.
    planetMercuryGlyphUnicodeKey = \
        "ui/astrology/mercuryGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mercury.
    planetMercuryGlyphUnicodeDefValue = "\u263f"

    # QSettings key for the planet glyph font size of the Mercury.
    planetMercuryGlyphFontSizeKey = \
        "ui/astrology/mercuryGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mercury.
    planetMercuryGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mercury.
    planetMercuryAbbreviationKey = \
        "ui/astrology/mercuryAbbreviation"

    # QSettings default value for the planet abbreviation of the Mercury.
    planetMercuryAbbreviationDefValue = "Me"

    # QSettings key for the foreground color of the Mercury.
    planetMercuryForegroundColorKey = \
        "ui/astrology/mercuryForegroundColor"

    # QSettings default value for the foreground color of the Mercury.
    planetMercuryForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mercury.
    planetMercuryBackgroundColorKey = \
        "ui/astrology/mercuryBackgroundColor"

    # QSettings default value for the background color of the Mercury.
    planetMercuryBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Venus.
    planetVenusGlyphUnicodeKey = \
        "ui/astrology/venusGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Venus.
    planetVenusGlyphUnicodeDefValue = "\u2640"

    # QSettings key for the planet glyph font size of the Venus.
    planetVenusGlyphFontSizeKey = \
        "ui/astrology/venusGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Venus.
    planetVenusGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Venus.
    planetVenusAbbreviationKey = \
        "ui/astrology/venusAbbreviation"

    # QSettings default value for the planet abbreviation of the Venus.
    planetVenusAbbreviationDefValue = "Ve"

    # QSettings key for the foreground color of the Venus.
    planetVenusForegroundColorKey = \
        "ui/astrology/venusForegroundColor"

    # QSettings default value for the foreground color of the Venus.
    planetVenusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Venus.
    planetVenusBackgroundColorKey = \
        "ui/astrology/venusBackgroundColor"

    # QSettings default value for the background color of the Venus.
    planetVenusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Earth.
    planetEarthGlyphUnicodeKey = \
        "ui/astrology/earthGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Earth.
    planetEarthGlyphUnicodeDefValue = "\u2d32"

    # QSettings key for the planet glyph font size of the Earth.
    planetEarthGlyphFontSizeKey = \
        "ui/astrology/earthGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Earth.
    planetEarthGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Earth.
    planetEarthAbbreviationKey = \
        "ui/astrology/earthAbbreviation"

    # QSettings default value for the planet abbreviation of the Earth.
    planetEarthAbbreviationDefValue = "Ea"

    # QSettings key for the foreground color of the Earth.
    planetEarthForegroundColorKey = \
        "ui/astrology/earthForegroundColor"

    # QSettings default value for the foreground color of the Earth.
    planetEarthForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Earth.
    planetEarthBackgroundColorKey = \
        "ui/astrology/earthBackgroundColor"

    # QSettings default value for the background color of the Earth.
    planetEarthBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mars.
    planetMarsGlyphUnicodeKey = \
        "ui/astrology/marsGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mars.
    planetMarsGlyphUnicodeDefValue = "\u2642"

    # QSettings key for the planet glyph font size of the Mars.
    planetMarsGlyphFontSizeKey = \
        "ui/astrology/marsGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mars.
    planetMarsGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mars.
    planetMarsAbbreviationKey = \
        "ui/astrology/marsAbbreviation"

    # QSettings default value for the planet abbreviation of the Mars.
    planetMarsAbbreviationDefValue = "Ma"

    # QSettings key for the foreground color of the Mars.
    planetMarsForegroundColorKey = \
        "ui/astrology/marsForegroundColor"

    # QSettings default value for the foreground color of the Mars.
    planetMarsForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mars.
    planetMarsBackgroundColorKey = \
        "ui/astrology/marsBackgroundColor"

    # QSettings default value for the background color of the Mars.
    planetMarsBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Jupiter.
    planetJupiterGlyphUnicodeKey = \
        "ui/astrology/jupiterGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Jupiter.
    planetJupiterGlyphUnicodeDefValue = "\u2643"

    # QSettings key for the planet glyph font size of the Jupiter.
    planetJupiterGlyphFontSizeKey = \
        "ui/astrology/jupiterGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Jupiter.
    planetJupiterGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Jupiter.
    planetJupiterAbbreviationKey = \
        "ui/astrology/jupiterAbbreviation"

    # QSettings default value for the planet abbreviation of the Jupiter.
    planetJupiterAbbreviationDefValue = "Ju"

    # QSettings key for the foreground color of the Jupiter.
    planetJupiterForegroundColorKey = \
        "ui/astrology/jupiterForegroundColor"

    # QSettings default value for the foreground color of the Jupiter.
    planetJupiterForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Jupiter.
    planetJupiterBackgroundColorKey = \
        "ui/astrology/jupiterBackgroundColor"

    # QSettings default value for the background color of the Jupiter.
    planetJupiterBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Saturn.
    planetSaturnGlyphUnicodeKey = \
        "ui/astrology/saturnGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Saturn.
    planetSaturnGlyphUnicodeDefValue = "\u2644"

    # QSettings key for the planet glyph font size of the Saturn.
    planetSaturnGlyphFontSizeKey = \
        "ui/astrology/saturnGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Saturn.
    planetSaturnGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Saturn.
    planetSaturnAbbreviationKey = \
        "ui/astrology/saturnAbbreviation"

    # QSettings default value for the planet abbreviation of the Saturn.
    planetSaturnAbbreviationDefValue = "Sa"

    # QSettings key for the foreground color of the Saturn.
    planetSaturnForegroundColorKey = \
        "ui/astrology/saturnForegroundColor"

    # QSettings default value for the foreground color of the Saturn.
    planetSaturnForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Saturn.
    planetSaturnBackgroundColorKey = \
        "ui/astrology/saturnBackgroundColor"

    # QSettings default value for the background color of the Saturn.
    planetSaturnBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Uranus.
    planetUranusGlyphUnicodeKey = \
        "ui/astrology/uranusGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Uranus.
    planetUranusGlyphUnicodeDefValue = "\u2645"

    # QSettings key for the planet glyph font size of the Uranus.
    planetUranusGlyphFontSizeKey = \
        "ui/astrology/uranusGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Uranus.
    planetUranusGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Uranus.
    planetUranusAbbreviationKey = \
        "ui/astrology/uranusAbbreviation"

    # QSettings default value for the planet abbreviation of the Uranus.
    planetUranusAbbreviationDefValue = "Ur"

    # QSettings key for the foreground color of the Uranus.
    planetUranusForegroundColorKey = \
        "ui/astrology/uranusForegroundColor"

    # QSettings default value for the foreground color of the Uranus.
    planetUranusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Uranus.
    planetUranusBackgroundColorKey = \
        "ui/astrology/uranusBackgroundColor"

    # QSettings default value for the background color of the Uranus.
    planetUranusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Neptune.
    planetNeptuneGlyphUnicodeKey = \
        "ui/astrology/neptuneGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Neptune.
    planetNeptuneGlyphUnicodeDefValue = "\u2646"

    # QSettings key for the planet glyph font size of the Neptune.
    planetNeptuneGlyphFontSizeKey = \
        "ui/astrology/neptuneGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Neptune.
    planetNeptuneGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Neptune.
    planetNeptuneAbbreviationKey = \
        "ui/astrology/neptuneAbbreviation"

    # QSettings default value for the planet abbreviation of the Neptune.
    planetNeptuneAbbreviationDefValue = "Ne"

    # QSettings key for the foreground color of the Neptune.
    planetNeptuneForegroundColorKey = \
        "ui/astrology/neptuneForegroundColor"

    # QSettings default value for the foreground color of the Neptune.
    planetNeptuneForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Neptune.
    planetNeptuneBackgroundColorKey = \
        "ui/astrology/neptuneBackgroundColor"

    # QSettings default value for the background color of the Neptune.
    planetNeptuneBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Pluto.
    planetPlutoGlyphUnicodeKey = \
        "ui/astrology/plutoGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Pluto.
    planetPlutoGlyphUnicodeDefValue = "\u2647"

    # QSettings key for the planet glyph font size of the Pluto.
    planetPlutoGlyphFontSizeKey = \
        "ui/astrology/plutoGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Pluto.
    planetPlutoGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Pluto.
    planetPlutoAbbreviationKey = \
        "ui/astrology/plutoAbbreviation"

    # QSettings default value for the planet abbreviation of the Pluto.
    planetPlutoAbbreviationDefValue = "Pl"

    # QSettings key for the foreground color of the Pluto.
    planetPlutoForegroundColorKey = \
        "ui/astrology/plutoForegroundColor"

    # QSettings default value for the foreground color of the Pluto.
    planetPlutoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pluto.
    planetPlutoBackgroundColorKey = \
        "ui/astrology/plutoBackgroundColor"

    # QSettings default value for the background color of the Pluto.
    planetPlutoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanNorthNode.
    planetMeanNorthNodeGlyphUnicodeKey = \
        "ui/astrology/meanNorthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanNorthNode.
    planetMeanNorthNodeGlyphUnicodeDefValue = "\u260a"

    # QSettings key for the planet glyph font size of the MeanNorthNode.
    planetMeanNorthNodeGlyphFontSizeKey = \
        "ui/astrology/meanNorthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanNorthNode.
    planetMeanNorthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanNorthNode.
    planetMeanNorthNodeAbbreviationKey = \
        "ui/astrology/meanNorthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanNorthNode.
    planetMeanNorthNodeAbbreviationDefValue = "Ra"

    # QSettings key for the foreground color of the MeanNorthNode.
    planetMeanNorthNodeForegroundColorKey = \
        "ui/astrology/meanNorthNodeForegroundColor"

    # QSettings default value for the foreground color of the MeanNorthNode.
    planetMeanNorthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanNorthNode.
    planetMeanNorthNodeBackgroundColorKey = \
        "ui/astrology/meanNorthNodeBackgroundColor"

    # QSettings default value for the background color of the MeanNorthNode.
    planetMeanNorthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanSouthNode.
    planetMeanSouthNodeGlyphUnicodeKey = \
        "ui/astrology/meanSouthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanSouthNode.
    planetMeanSouthNodeGlyphUnicodeDefValue = "\u260b"

    # QSettings key for the planet glyph font size of the MeanSouthNode.
    planetMeanSouthNodeGlyphFontSizeKey = \
        "ui/astrology/meanSouthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanSouthNode.
    planetMeanSouthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanSouthNode.
    planetMeanSouthNodeAbbreviationKey = \
        "ui/astrology/meanSouthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanSouthNode.
    planetMeanSouthNodeAbbreviationDefValue = "Ke"

    # QSettings key for the foreground color of the MeanSouthNode.
    planetMeanSouthNodeForegroundColorKey = \
        "ui/astrology/meanSouthNodeForegroundColor"

    # QSettings default value for the foreground color of the MeanSouthNode.
    planetMeanSouthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanSouthNode.
    planetMeanSouthNodeBackgroundColorKey = \
        "ui/astrology/meanSouthNodeBackgroundColor"

    # QSettings default value for the background color of the MeanSouthNode.
    planetMeanSouthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the TrueNorthNode.
    planetTrueNorthNodeGlyphUnicodeKey = \
        "ui/astrology/trueNorthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the TrueNorthNode.
    planetTrueNorthNodeGlyphUnicodeDefValue = "\u260a"

    # QSettings key for the planet glyph font size of the TrueNorthNode.
    planetTrueNorthNodeGlyphFontSizeKey = \
        "ui/astrology/trueNorthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the TrueNorthNode.
    planetTrueNorthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the TrueNorthNode.
    planetTrueNorthNodeAbbreviationKey = \
        "ui/astrology/trueNorthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the TrueNorthNode.
    planetTrueNorthNodeAbbreviationDefValue = "TrueNNode"

    # QSettings key for the foreground color of the TrueNorthNode.
    planetTrueNorthNodeForegroundColorKey = \
        "ui/astrology/trueNorthNodeForegroundColor"

    # QSettings default value for the foreground color of the TrueNorthNode.
    planetTrueNorthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the TrueNorthNode.
    planetTrueNorthNodeBackgroundColorKey = \
        "ui/astrology/trueNorthNodeBackgroundColor"

    # QSettings default value for the background color of the TrueNorthNode.
    planetTrueNorthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the TrueSouthNode.
    planetTrueSouthNodeGlyphUnicodeKey = \
        "ui/astrology/trueSouthNodeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the TrueSouthNode.
    planetTrueSouthNodeGlyphUnicodeDefValue = "\u260b"

    # QSettings key for the planet glyph font size of the TrueSouthNode.
    planetTrueSouthNodeGlyphFontSizeKey = \
        "ui/astrology/trueSouthNodeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the TrueSouthNode.
    planetTrueSouthNodeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the TrueSouthNode.
    planetTrueSouthNodeAbbreviationKey = \
        "ui/astrology/trueSouthNodeAbbreviation"

    # QSettings default value for the planet abbreviation of the TrueSouthNode.
    planetTrueSouthNodeAbbreviationDefValue = "TrueSNode"

    # QSettings key for the foreground color of the TrueSouthNode.
    planetTrueSouthNodeForegroundColorKey = \
        "ui/astrology/trueSouthNodeForegroundColor"

    # QSettings default value for the foreground color of the TrueSouthNode.
    planetTrueSouthNodeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the TrueSouthNode.
    planetTrueSouthNodeBackgroundColorKey = \
        "ui/astrology/trueSouthNodeBackgroundColor"

    # QSettings default value for the background color of the TrueSouthNode.
    planetTrueSouthNodeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Ceres.
    planetCeresGlyphUnicodeKey = \
        "ui/astrology/ceresGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Ceres.
    planetCeresGlyphUnicodeDefValue = "\u26b3"

    # QSettings key for the planet glyph font size of the Ceres.
    planetCeresGlyphFontSizeKey = \
        "ui/astrology/ceresGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Ceres.
    planetCeresGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Ceres.
    planetCeresAbbreviationKey = \
        "ui/astrology/ceresAbbreviation"

    # QSettings default value for the planet abbreviation of the Ceres.
    planetCeresAbbreviationDefValue = "Ce"

    # QSettings key for the foreground color of the Ceres.
    planetCeresForegroundColorKey = \
        "ui/astrology/ceresForegroundColor"

    # QSettings default value for the foreground color of the Ceres.
    planetCeresForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Ceres.
    planetCeresBackgroundColorKey = \
        "ui/astrology/ceresBackgroundColor"

    # QSettings default value for the background color of the Ceres.
    planetCeresBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Pallas.
    planetPallasGlyphUnicodeKey = \
        "ui/astrology/pallasGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Pallas.
    planetPallasGlyphUnicodeDefValue = "\u26b4"

    # QSettings key for the planet glyph font size of the Pallas.
    planetPallasGlyphFontSizeKey = \
        "ui/astrology/pallasGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Pallas.
    planetPallasGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Pallas.
    planetPallasAbbreviationKey = \
        "ui/astrology/pallasAbbreviation"

    # QSettings default value for the planet abbreviation of the Pallas.
    planetPallasAbbreviationDefValue = "Pa"

    # QSettings key for the foreground color of the Pallas.
    planetPallasForegroundColorKey = \
        "ui/astrology/pallasForegroundColor"

    # QSettings default value for the foreground color of the Pallas.
    planetPallasForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pallas.
    planetPallasBackgroundColorKey = \
        "ui/astrology/pallasBackgroundColor"

    # QSettings default value for the background color of the Pallas.
    planetPallasBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Juno.
    planetJunoGlyphUnicodeKey = \
        "ui/astrology/junoGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Juno.
    planetJunoGlyphUnicodeDefValue = "\u26b5"

    # QSettings key for the planet glyph font size of the Juno.
    planetJunoGlyphFontSizeKey = \
        "ui/astrology/junoGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Juno.
    planetJunoGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Juno.
    planetJunoAbbreviationKey = \
        "ui/astrology/junoAbbreviation"

    # QSettings default value for the planet abbreviation of the Juno.
    planetJunoAbbreviationDefValue = "Jun"

    # QSettings key for the foreground color of the Juno.
    planetJunoForegroundColorKey = \
        "ui/astrology/junoForegroundColor"

    # QSettings default value for the foreground color of the Juno.
    planetJunoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Juno.
    planetJunoBackgroundColorKey = \
        "ui/astrology/junoBackgroundColor"

    # QSettings default value for the background color of the Juno.
    planetJunoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Vesta.
    planetVestaGlyphUnicodeKey = \
        "ui/astrology/vestaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Vesta.
    planetVestaGlyphUnicodeDefValue = "\u26b6"

    # QSettings key for the planet glyph font size of the Vesta.
    planetVestaGlyphFontSizeKey = \
        "ui/astrology/vestaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Vesta.
    planetVestaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Vesta.
    planetVestaAbbreviationKey = \
        "ui/astrology/vestaAbbreviation"

    # QSettings default value for the planet abbreviation of the Vesta.
    planetVestaAbbreviationDefValue = "Ves"

    # QSettings key for the foreground color of the Vesta.
    planetVestaForegroundColorKey = \
        "ui/astrology/vestaForegroundColor"

    # QSettings default value for the foreground color of the Vesta.
    planetVestaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Vesta.
    planetVestaBackgroundColorKey = \
        "ui/astrology/vestaBackgroundColor"

    # QSettings default value for the background color of the Vesta.
    planetVestaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Isis.
    planetIsisGlyphUnicodeKey = \
        "ui/astrology/isisGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Isis.
    planetIsisGlyphUnicodeDefValue = "\u26b6"

    # QSettings key for the planet glyph font size of the Isis.
    planetIsisGlyphFontSizeKey = \
        "ui/astrology/isisGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Isis.
    planetIsisGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Isis.
    planetIsisAbbreviationKey = \
        "ui/astrology/isisAbbreviation"

    # QSettings default value for the planet abbreviation of the Isis.
    planetIsisAbbreviationDefValue = "Ves"

    # QSettings key for the foreground color of the Isis.
    planetIsisForegroundColorKey = \
        "ui/astrology/isisForegroundColor"

    # QSettings default value for the foreground color of the Isis.
    planetIsisForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Isis.
    planetIsisBackgroundColorKey = \
        "ui/astrology/isisBackgroundColor"

    # QSettings default value for the background color of the Isis.
    planetIsisBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Nibiru.
    planetNibiruGlyphUnicodeKey = \
        "ui/astrology/nibiruGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Nibiru.
    planetNibiruGlyphUnicodeDefValue = "\u26b6"

    # QSettings key for the planet glyph font size of the Nibiru.
    planetNibiruGlyphFontSizeKey = \
        "ui/astrology/nibiruGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Nibiru.
    planetNibiruGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Nibiru.
    planetNibiruAbbreviationKey = \
        "ui/astrology/nibiruAbbreviation"

    # QSettings default value for the planet abbreviation of the Nibiru.
    planetNibiruAbbreviationDefValue = "Ves"

    # QSettings key for the foreground color of the Nibiru.
    planetNibiruForegroundColorKey = \
        "ui/astrology/nibiruForegroundColor"

    # QSettings default value for the foreground color of the Nibiru.
    planetNibiruForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Nibiru.
    planetNibiruBackgroundColorKey = \
        "ui/astrology/nibiruBackgroundColor"

    # QSettings default value for the background color of the Nibiru.
    planetNibiruBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Chiron.
    planetChironGlyphUnicodeKey = \
        "ui/astrology/chironGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Chiron.
    planetChironGlyphUnicodeDefValue = "\u26b7"

    # QSettings key for the planet glyph font size of the Chiron.
    planetChironGlyphFontSizeKey = \
        "ui/astrology/chironGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Chiron.
    planetChironGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Chiron.
    planetChironAbbreviationKey = \
        "ui/astrology/chironAbbreviation"

    # QSettings default value for the planet abbreviation of the Chiron.
    planetChironAbbreviationDefValue = "Chi"

    # QSettings key for the foreground color of the Chiron.
    planetChironForegroundColorKey = \
        "ui/astrology/chironForegroundColor"

    # QSettings default value for the foreground color of the Chiron.
    planetChironForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Chiron.
    planetChironBackgroundColorKey = \
        "ui/astrology/chironBackgroundColor"

    # QSettings default value for the background color of the Chiron.
    planetChironBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Gulika.
    planetGulikaGlyphUnicodeKey = \
        "ui/astrology/gulikaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Gulika.
    planetGulikaGlyphUnicodeDefValue = "Gk"

    # QSettings key for the planet glyph font size of the Gulika.
    planetGulikaGlyphFontSizeKey = \
        "ui/astrology/gulikaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Gulika.
    planetGulikaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Gulika.
    planetGulikaAbbreviationKey = \
        "ui/astrology/gulikaAbbreviation"

    # QSettings default value for the planet abbreviation of the Gulika.
    planetGulikaAbbreviationDefValue = "Gk"

    # QSettings key for the foreground color of the Gulika.
    planetGulikaForegroundColorKey = \
        "ui/astrology/gulikaForegroundColor"

    # QSettings default value for the foreground color of the Gulika.
    planetGulikaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Gulika.
    planetGulikaBackgroundColorKey = \
        "ui/astrology/gulikaBackgroundColor"

    # QSettings default value for the background color of the Gulika.
    planetGulikaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the Mandi.
    planetMandiGlyphUnicodeKey = \
        "ui/astrology/mandiGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the Mandi.
    planetMandiGlyphUnicodeDefValue = "Md"

    # QSettings key for the planet glyph font size of the Mandi.
    planetMandiGlyphFontSizeKey = \
        "ui/astrology/mandiGlyphFontSize"

    # QSettings default value for the planet glyph font size of the Mandi.
    planetMandiGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the Mandi.
    planetMandiAbbreviationKey = \
        "ui/astrology/mandiAbbreviation"

    # QSettings default value for the planet abbreviation of the Mandi.
    planetMandiAbbreviationDefValue = "Md"

    # QSettings key for the foreground color of the Mandi.
    planetMandiForegroundColorKey = \
        "ui/astrology/mandiForegroundColor"

    # QSettings default value for the foreground color of the Mandi.
    planetMandiForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Mandi.
    planetMandiBackgroundColorKey = \
        "ui/astrology/mandiBackgroundColor"

    # QSettings default value for the background color of the Mandi.
    planetMandiBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the MeanOfFive.
    planetMeanOfFiveGlyphUnicodeKey = \
        "ui/astrology/meanOfFiveGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the MeanOfFive.
    planetMeanOfFiveGlyphUnicodeDefValue = "MOF"

    # QSettings key for the planet glyph font size of the MeanOfFive.
    planetMeanOfFiveGlyphFontSizeKey = \
        "ui/astrology/meanOfFiveGlyphFontSize"

    # QSettings default value for the planet glyph font size of the MeanOfFive.
    planetMeanOfFiveGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the MeanOfFive.
    planetMeanOfFiveAbbreviationKey = \
        "ui/astrology/meanOfFiveAbbreviation"

    # QSettings default value for the planet abbreviation of the MeanOfFive.
    planetMeanOfFiveAbbreviationDefValue = "MOF"

    # QSettings key for the foreground color of the MeanOfFive.
    planetMeanOfFiveForegroundColorKey = \
        "ui/astrology/meanOfFiveForegroundColor"

    # QSettings default value for the foreground color of the MeanOfFive.
    planetMeanOfFiveForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the MeanOfFive.
    planetMeanOfFiveBackgroundColorKey = \
        "ui/astrology/meanOfFiveBackgroundColor"

    # QSettings default value for the background color of the MeanOfFive.
    planetMeanOfFiveBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the CycleOfEight.
    planetCycleOfEightGlyphUnicodeKey = \
        "ui/astrology/cycleOfEightGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the CycleOfEight.
    planetCycleOfEightGlyphUnicodeDefValue = "COE"

    # QSettings key for the planet glyph font size of the CycleOfEight.
    planetCycleOfEightGlyphFontSizeKey = \
        "ui/astrology/cycleOfEightGlyphFontSize"

    # QSettings default value for the planet glyph font size of the CycleOfEight.
    planetCycleOfEightGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the CycleOfEight.
    planetCycleOfEightAbbreviationKey = \
        "ui/astrology/cycleOfEightAbbreviation"

    # QSettings default value for the planet abbreviation of the CycleOfEight.
    planetCycleOfEightAbbreviationDefValue = "COE"

    # QSettings key for the foreground color of the CycleOfEight.
    planetCycleOfEightForegroundColorKey = \
        "ui/astrology/cycleOfEightForegroundColor"

    # QSettings default value for the foreground color of the CycleOfEight.
    planetCycleOfEightForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the CycleOfEight.
    planetCycleOfEightBackgroundColorKey = \
        "ui/astrology/cycleOfEightBackgroundColor"

    # QSettings default value for the background color of the CycleOfEight.
    planetCycleOfEightBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphUnicodeKey = \
        "ui/astrology/avgMaJuSaUrNePlGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphUnicodeDefValue = "AvgMaJuSaUrNePl"

    # QSettings key for the planet glyph font size of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphFontSizeKey = \
        "ui/astrology/avgMaJuSaUrNePlGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlAbbreviationKey = \
        "ui/astrology/avgMaJuSaUrNePlAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlAbbreviationDefValue = "AvgMaJuSaUrNePl"

    # QSettings key for the foreground color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlForegroundColorKey = \
        "ui/astrology/avgMaJuSaUrNePlForegroundColor"

    # QSettings default value for the foreground color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlBackgroundColorKey = \
        "ui/astrology/avgMaJuSaUrNePlBackgroundColor"

    # QSettings default value for the background color of the AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphUnicodeKey = \
        "ui/astrology/avgJuSaUrNeGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphUnicodeDefValue = "AvgJuSaUrNe"

    # QSettings key for the planet glyph font size of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphFontSizeKey = \
        "ui/astrology/avgJuSaUrNeGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgJuSaUrNe.
    planetAvgJuSaUrNeGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgJuSaUrNe.
    planetAvgJuSaUrNeAbbreviationKey = \
        "ui/astrology/avgJuSaUrNeAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgJuSaUrNe.
    planetAvgJuSaUrNeAbbreviationDefValue = "AvgJuSaUrNe"

    # QSettings key for the foreground color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeForegroundColorKey = \
        "ui/astrology/avgJuSaUrNeForegroundColor"

    # QSettings default value for the foreground color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeBackgroundColorKey = \
        "ui/astrology/avgJuSaUrNeBackgroundColor"

    # QSettings default value for the background color of the AvgJuSaUrNe.
    planetAvgJuSaUrNeBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the planet glyph unicode of the AvgJuSa.
    planetAvgJuSaGlyphUnicodeKey = \
        "ui/astrology/avgJuSaGlyphUnicode"

    # QSettings default value for the planet glyph unicode of the AvgJuSa.
    planetAvgJuSaGlyphUnicodeDefValue = "AvgJuSa"

    # QSettings key for the planet glyph font size of the AvgJuSa.
    planetAvgJuSaGlyphFontSizeKey = \
        "ui/astrology/avgJuSaGlyphFontSize"

    # QSettings default value for the planet glyph font size of the AvgJuSa.
    planetAvgJuSaGlyphFontSizeDefValue = 10

    # QSettings key for the planet abbreviation of the AvgJuSa.
    planetAvgJuSaAbbreviationKey = \
        "ui/astrology/avgJuSaAbbreviation"

    # QSettings default value for the planet abbreviation of the AvgJuSa.
    planetAvgJuSaAbbreviationDefValue = "AvgJuSa"

    # QSettings key for the foreground color of the AvgJuSa.
    planetAvgJuSaForegroundColorKey = \
        "ui/astrology/avgJuSaForegroundColor"

    # QSettings default value for the foreground color of the AvgJuSa.
    planetAvgJuSaForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the AvgJuSa.
    planetAvgJuSaBackgroundColorKey = \
        "ui/astrology/avgJuSaBackgroundColor"

    # QSettings default value for the background color of the AvgJuSa.
    planetAvgJuSaBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Aries.
    signAriesGlyphUnicodeKey = \
        "ui/astrology/ariesGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Aries.
    signAriesGlyphUnicodeDefValue = "\u2648"

    # QSettings key for the sign glyph font size of the Aries.
    signAriesGlyphFontSizeKey = \
        "ui/astrology/ariesGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Aries.
    signAriesGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Aries.
    signAriesAbbreviationKey = \
        "ui/astrology/ariesAbbreviation"

    # QSettings default value for the sign abbreviation of the Aries.
    signAriesAbbreviationDefValue = "Ar"

    # QSettings key for the foreground color of the Aries.
    signAriesForegroundColorKey = \
        "ui/astrology/ariesForegroundColor"

    # QSettings default value for the foreground color of the Aries.
    signAriesForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Aries.
    signAriesBackgroundColorKey = \
        "ui/astrology/ariesBackgroundColor"

    # QSettings default value for the background color of the Aries.
    signAriesBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Taurus.
    signTaurusGlyphUnicodeKey = \
        "ui/astrology/taurusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Taurus.
    signTaurusGlyphUnicodeDefValue = "\u2649"

    # QSettings key for the sign glyph font size of the Taurus.
    signTaurusGlyphFontSizeKey = \
        "ui/astrology/taurusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Taurus.
    signTaurusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Taurus.
    signTaurusAbbreviationKey = \
        "ui/astrology/taurusAbbreviation"

    # QSettings default value for the sign abbreviation of the Taurus.
    signTaurusAbbreviationDefValue = "Ta"

    # QSettings key for the foreground color of the Taurus.
    signTaurusForegroundColorKey = \
        "ui/astrology/taurusForegroundColor"

    # QSettings default value for the foreground color of the Taurus.
    signTaurusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Taurus.
    signTaurusBackgroundColorKey = \
        "ui/astrology/taurusBackgroundColor"

    # QSettings default value for the background color of the Taurus.
    signTaurusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Gemini.
    signGeminiGlyphUnicodeKey = \
        "ui/astrology/geminiGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Gemini.
    signGeminiGlyphUnicodeDefValue = "\u264a"

    # QSettings key for the sign glyph font size of the Gemini.
    signGeminiGlyphFontSizeKey = \
        "ui/astrology/geminiGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Gemini.
    signGeminiGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Gemini.
    signGeminiAbbreviationKey = \
        "ui/astrology/geminiAbbreviation"

    # QSettings default value for the sign abbreviation of the Gemini.
    signGeminiAbbreviationDefValue = "Ge"

    # QSettings key for the foreground color of the Gemini.
    signGeminiForegroundColorKey = \
        "ui/astrology/geminiForegroundColor"

    # QSettings default value for the foreground color of the Gemini.
    signGeminiForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Gemini.
    signGeminiBackgroundColorKey = \
        "ui/astrology/geminiBackgroundColor"

    # QSettings default value for the background color of the Gemini.
    signGeminiBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Cancer.
    signCancerGlyphUnicodeKey = \
        "ui/astrology/cancerGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Cancer.
    signCancerGlyphUnicodeDefValue = "\u264b"

    # QSettings key for the sign glyph font size of the Cancer.
    signCancerGlyphFontSizeKey = \
        "ui/astrology/cancerGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Cancer.
    signCancerGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Cancer.
    signCancerAbbreviationKey = \
        "ui/astrology/cancerAbbreviation"

    # QSettings default value for the sign abbreviation of the Cancer.
    signCancerAbbreviationDefValue = "Ca"

    # QSettings key for the foreground color of the Cancer.
    signCancerForegroundColorKey = \
        "ui/astrology/cancerForegroundColor"

    # QSettings default value for the foreground color of the Cancer.
    signCancerForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Cancer.
    signCancerBackgroundColorKey = \
        "ui/astrology/cancerBackgroundColor"

    # QSettings default value for the background color of the Cancer.
    signCancerBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Leo.
    signLeoGlyphUnicodeKey = \
        "ui/astrology/leoGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Leo.
    signLeoGlyphUnicodeDefValue = "\u264c"

    # QSettings key for the sign glyph font size of the Leo.
    signLeoGlyphFontSizeKey = \
        "ui/astrology/leoGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Leo.
    signLeoGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Leo.
    signLeoAbbreviationKey = \
        "ui/astrology/leoAbbreviation"

    # QSettings default value for the sign abbreviation of the Leo.
    signLeoAbbreviationDefValue = "Le"

    # QSettings key for the foreground color of the Leo.
    signLeoForegroundColorKey = \
        "ui/astrology/leoForegroundColor"

    # QSettings default value for the foreground color of the Leo.
    signLeoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Leo.
    signLeoBackgroundColorKey = \
        "ui/astrology/leoBackgroundColor"

    # QSettings default value for the background color of the Leo.
    signLeoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Virgo.
    signVirgoGlyphUnicodeKey = \
        "ui/astrology/virgoGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Virgo.
    signVirgoGlyphUnicodeDefValue = "\u264d"

    # QSettings key for the sign glyph font size of the Virgo.
    signVirgoGlyphFontSizeKey = \
        "ui/astrology/virgoGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Virgo.
    signVirgoGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Virgo.
    signVirgoAbbreviationKey = \
        "ui/astrology/virgoAbbreviation"

    # QSettings default value for the sign abbreviation of the Virgo.
    signVirgoAbbreviationDefValue = "Vi"

    # QSettings key for the foreground color of the Virgo.
    signVirgoForegroundColorKey = \
        "ui/astrology/virgoForegroundColor"

    # QSettings default value for the foreground color of the Virgo.
    signVirgoForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Virgo.
    signVirgoBackgroundColorKey = \
        "ui/astrology/virgoBackgroundColor"

    # QSettings default value for the background color of the Virgo.
    signVirgoBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Libra.
    signLibraGlyphUnicodeKey = \
        "ui/astrology/libraGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Libra.
    signLibraGlyphUnicodeDefValue = "\u264e"

    # QSettings key for the sign glyph font size of the Libra.
    signLibraGlyphFontSizeKey = \
        "ui/astrology/libraGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Libra.
    signLibraGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Libra.
    signLibraAbbreviationKey = \
        "ui/astrology/libraAbbreviation"

    # QSettings default value for the sign abbreviation of the Libra.
    signLibraAbbreviationDefValue = "Li"

    # QSettings key for the foreground color of the Libra.
    signLibraForegroundColorKey = \
        "ui/astrology/libraForegroundColor"

    # QSettings default value for the foreground color of the Libra.
    signLibraForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Libra.
    signLibraBackgroundColorKey = \
        "ui/astrology/libraBackgroundColor"

    # QSettings default value for the background color of the Libra.
    signLibraBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Scorpio.
    signScorpioGlyphUnicodeKey = \
        "ui/astrology/scorpioGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Scorpio.
    signScorpioGlyphUnicodeDefValue = "\u264f"

    # QSettings key for the sign glyph font size of the Scorpio.
    signScorpioGlyphFontSizeKey = \
        "ui/astrology/scorpioGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Scorpio.
    signScorpioGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Scorpio.
    signScorpioAbbreviationKey = \
        "ui/astrology/scorpioAbbreviation"

    # QSettings default value for the sign abbreviation of the Scorpio.
    signScorpioAbbreviationDefValue = "Sc"

    # QSettings key for the foreground color of the Scorpio.
    signScorpioForegroundColorKey = \
        "ui/astrology/scorpioForegroundColor"

    # QSettings default value for the foreground color of the Scorpio.
    signScorpioForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Scorpio.
    signScorpioBackgroundColorKey = \
        "ui/astrology/scorpioBackgroundColor"

    # QSettings default value for the background color of the Scorpio.
    signScorpioBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Sagittarius.
    signSagittariusGlyphUnicodeKey = \
        "ui/astrology/sagittariusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Sagittarius.
    signSagittariusGlyphUnicodeDefValue = "\u2650"

    # QSettings key for the sign glyph font size of the Sagittarius.
    signSagittariusGlyphFontSizeKey = \
        "ui/astrology/sagittariusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Sagittarius.
    signSagittariusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Sagittarius.
    signSagittariusAbbreviationKey = \
        "ui/astrology/sagittariusAbbreviation"

    # QSettings default value for the sign abbreviation of the Sagittarius.
    signSagittariusAbbreviationDefValue = "Sa"

    # QSettings key for the foreground color of the Sagittarius.
    signSagittariusForegroundColorKey = \
        "ui/astrology/sagittariusForegroundColor"

    # QSettings default value for the foreground color of the Sagittarius.
    signSagittariusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Sagittarius.
    signSagittariusBackgroundColorKey = \
        "ui/astrology/sagittariusBackgroundColor"

    # QSettings default value for the background color of the Sagittarius.
    signSagittariusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Capricorn.
    signCapricornGlyphUnicodeKey = \
        "ui/astrology/capricornGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Capricorn.
    signCapricornGlyphUnicodeDefValue = "\u2651"

    # QSettings key for the sign glyph font size of the Capricorn.
    signCapricornGlyphFontSizeKey = \
        "ui/astrology/capricornGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Capricorn.
    signCapricornGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Capricorn.
    signCapricornAbbreviationKey = \
        "ui/astrology/capricornAbbreviation"

    # QSettings default value for the sign abbreviation of the Capricorn.
    signCapricornAbbreviationDefValue = "Cp"

    # QSettings key for the foreground color of the Capricorn.
    signCapricornForegroundColorKey = \
        "ui/astrology/capricornForegroundColor"

    # QSettings default value for the foreground color of the Capricorn.
    signCapricornForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Capricorn.
    signCapricornBackgroundColorKey = \
        "ui/astrology/capricornBackgroundColor"

    # QSettings default value for the background color of the Capricorn.
    signCapricornBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Aquarius.
    signAquariusGlyphUnicodeKey = \
        "ui/astrology/aquariusGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Aquarius.
    signAquariusGlyphUnicodeDefValue = "\u2652"

    # QSettings key for the sign glyph font size of the Aquarius.
    signAquariusGlyphFontSizeKey = \
        "ui/astrology/aquariusGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Aquarius.
    signAquariusGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Aquarius.
    signAquariusAbbreviationKey = \
        "ui/astrology/aquariusAbbreviation"

    # QSettings default value for the sign abbreviation of the Aquarius.
    signAquariusAbbreviationDefValue = "Aq"

    # QSettings key for the foreground color of the Aquarius.
    signAquariusForegroundColorKey = \
        "ui/astrology/aquariusForegroundColor"

    # QSettings default value for the foreground color of the Aquarius.
    signAquariusForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Aquarius.
    signAquariusBackgroundColorKey = \
        "ui/astrology/aquariusBackgroundColor"

    # QSettings default value for the background color of the Aquarius.
    signAquariusBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for the sign glyph unicode of the Pisces.
    signPiscesGlyphUnicodeKey = \
        "ui/astrology/piscesGlyphUnicode"

    # QSettings default value for the sign glyph unicode of the Pisces.
    signPiscesGlyphUnicodeDefValue = "\u2653"

    # QSettings key for the sign glyph font size of the Pisces.
    signPiscesGlyphFontSizeKey = \
        "ui/astrology/piscesGlyphFontSize"

    # QSettings default value for the sign glyph font size of the Pisces.
    signPiscesGlyphFontSizeDefValue = 10

    # QSettings key for the sign abbreviation of the Pisces.
    signPiscesAbbreviationKey = \
        "ui/astrology/piscesAbbreviation"

    # QSettings default value for the sign abbreviation of the Pisces.
    signPiscesAbbreviationDefValue = "Pi"

    # QSettings key for the foreground color of the Pisces.
    signPiscesForegroundColorKey = \
        "ui/astrology/piscesForegroundColor"

    # QSettings default value for the foreground color of the Pisces.
    signPiscesForegroundColorDefValue = QColor(Qt.black)

    # QSettings key for the background color of the Pisces.
    signPiscesBackgroundColorKey = \
        "ui/astrology/piscesBackgroundColor"

    # QSettings default value for the background color of the Pisces.
    signPiscesBackgroundColorDefValue = QColor(Qt.transparent)



    # QSettings key for aspects enabled on astrology chart 1.
    aspectAstrologyChart1EnabledKey = \
        "ui/astrology/aspectAstrologyChart1Enabled"

    # QSettings default value for aspect enabled on astrology chart 1.
    aspectAstrologyChart1EnabledDefValue = \
        True
    
    # QSettings key for aspects enabled on astrology chart 2.
    aspectAstrologyChart2EnabledKey = \
        "ui/astrology/aspectAstrologyChart2Enabled"

    # QSettings default value for aspect enabled on astrology chart 2.
    aspectAstrologyChart2EnabledDefValue = \
        True
    
    # QSettings key for aspects enabled on astrology chart 3.
    aspectAstrologyChart3EnabledKey = \
        "ui/astrology/aspectAstrologyChart3Enabled"

    # QSettings default value for aspect enabled on astrology chart 3.
    aspectAstrologyChart3EnabledDefValue = \
        True

    # QSettings key for aspects enabled between astrology chart 1 and 2.
    aspectBtwnAstrologyChart1And2EnabledKey = \
        "ui/astrology/aspectBtwnAstrologyChart1And2Enabled"
    
    # QSettings default value for aspects enabled between astrology chart 1 and 2.
    aspectBtwnAstrologyChart1And2EnabledDefValue = \
        False
    
    # QSettings key for aspects enabled between astrology chart 1 and 3.
    aspectBtwnAstrologyChart1And3EnabledKey = \
        "ui/astrology/aspectBtwnAstrologyChart1And3Enabled"
    
    # QSettings default value for aspects enabled between astrology chart 1 and 3.
    aspectBtwnAstrologyChart1And3EnabledDefValue = \
        False
    
    # QSettings key for aspects enabled between astrology chart 2 and 3.
    aspectBtwnAstrologyChart2And3EnabledKey = \
        "ui/astrology/aspectBtwnAstrologyChart2And3Enabled"
    
    # QSettings default value for aspects enabled between astrology chart 2 and 3.
    aspectBtwnAstrologyChart2And3EnabledDefValue = \
        False

    
    # QSettings key for the aspect Conjunction name.
    aspectConjunctionNameKey = \
        "ui/astrology/aspectConjunctionName"

    # QSettings default value for the aspect Conjunction name.
    aspectConjunctionNameDefValue = \
        "Conjunction"
    
    # QSettings key for the aspect Conjunction angle.
    aspectConjunctionAngleKey = \
        "ui/astrology/aspectConjunctionAngle"

    # QSettings default value for the aspect Conjunction angle (float).
    aspectConjunctionAngleDefValue = float(0.0)
    
    # QSettings key for the aspect Conjunction being enabled.
    aspectConjunctionEnabledKey = \
        "ui/astrology/aspectConjunctionEnabled"

    # QSettings default value for the aspect Conjunction being enabled.
    aspectConjunctionEnabledDefValue = True
    
    # QSettings key for the aspect Conjunction color.
    aspectConjunctionColorKey = \
        "ui/astrology/aspectConjunctionColor"

    # QSettings default value for the aspect Conjunction color.
    aspectConjunctionColorDefValue = QColor(Qt.darkYellow)

    # QSettings key for the aspect Conjunction orb in degrees.
    aspectConjunctionOrbKey = \
        "ui/astrology/aspectConjunctionOrb"

    # QSettings default value for the aspect Conjunction orb in degrees (float).
    aspectConjunctionOrbDefValue = float(6.0)


    
    # QSettings key for the aspect Opposition name.
    aspectOppositionNameKey = \
        "ui/astrology/aspectOppositionName"

    # QSettings default value for the aspect Opposition name.
    aspectOppositionNameDefValue = \
        "Opposition"
    
    # QSettings key for the aspect Opposition angle.
    aspectOppositionAngleKey = \
        "ui/astrology/aspectOppositionAngle"

    # QSettings default value for the aspect Opposition angle (float).
    aspectOppositionAngleDefValue = float(180.0)
    
    # QSettings key for the aspect Opposition being enabled.
    aspectOppositionEnabledKey = \
        "ui/astrology/aspectOppositionEnabled"

    # QSettings default value for the aspect Opposition being enabled.
    aspectOppositionEnabledDefValue = True
    
    # QSettings key for the aspect Opposition color.
    aspectOppositionColorKey = \
        "ui/astrology/aspectOppositionColor"

    # QSettings default value for the aspect Opposition color.
    aspectOppositionColorDefValue = QColor(Qt.blue)

    # QSettings key for the aspect Opposition orb in degrees.
    aspectOppositionOrbKey = \
        "ui/astrology/aspectOppositionOrb"

    # QSettings default value for the aspect Opposition orb in degrees (float).
    aspectOppositionOrbDefValue = float(6.0)



    # QSettings key for the aspect Square name.
    aspectSquareNameKey = \
        "ui/astrology/aspectSquareName"

    # QSettings default value for the aspect Square name.
    aspectSquareNameDefValue = \
        "Square"
    
    # QSettings key for the aspect Square angle.
    aspectSquareAngleKey = \
        "ui/astrology/aspectSquareAngle"

    # QSettings default value for the aspect Square angle (float).
    aspectSquareAngleDefValue = float(90.0)
    
    # QSettings key for the aspect Square being enabled.
    aspectSquareEnabledKey = \
        "ui/astrology/aspectSquareEnabled"

    # QSettings default value for the aspect Square being enabled.
    aspectSquareEnabledDefValue = True
    
    # QSettings key for the aspect Square color.
    aspectSquareColorKey = \
        "ui/astrology/aspectSquareColor"

    # QSettings default value for the aspect Square color.
    aspectSquareColorDefValue = QColor(Qt.red)

    # QSettings key for the aspect Square orb in degrees.
    aspectSquareOrbKey = \
        "ui/astrology/aspectSquareOrb"

    # QSettings default value for the aspect Square orb in degrees (float).
    aspectSquareOrbDefValue = float(6.0)



    # QSettings key for the aspect Trine name.
    aspectTrineNameKey = \
        "ui/astrology/aspectTrineName"

    # QSettings default value for the aspect Trine name.
    aspectTrineNameDefValue = \
        "Trine"
    
    # QSettings key for the aspect Trine angle.
    aspectTrineAngleKey = \
        "ui/astrology/aspectTrineAngle"

    # QSettings default value for the aspect Trine angle (float).
    aspectTrineAngleDefValue = float(120.0)
    
    # QSettings key for the aspect Trine being enabled.
    aspectTrineEnabledKey = \
        "ui/astrology/aspectTrineEnabled"

    # QSettings default value for the aspect Trine being enabled.
    aspectTrineEnabledDefValue = True
    
    # QSettings key for the aspect Trine color.
    aspectTrineColorKey = \
        "ui/astrology/aspectTrineColor"

    # QSettings default value for the aspect Trine color.
    aspectTrineColorDefValue = QColor(Qt.darkGreen)

    # QSettings key for the aspect Trine orb in degrees.
    aspectTrineOrbKey = \
        "ui/astrology/aspectTrineOrb"

    # QSettings default value for the aspect Trine orb in degrees (float).
    aspectTrineOrbDefValue = float(6.0)



    # QSettings key for the aspect Sextile name.
    aspectSextileNameKey = \
        "ui/astrology/aspectSextileName"

    # QSettings default value for the aspect Sextile name.
    aspectSextileNameDefValue = \
        "Sextile"
    
    # QSettings key for the aspect Sextile angle.
    aspectSextileAngleKey = \
        "ui/astrology/aspectSextileAngle"

    # QSettings default value for the aspect Sextile angle (float).
    aspectSextileAngleDefValue = float(60.0)
    
    # QSettings key for the aspect Sextile being enabled.
    aspectSextileEnabledKey = \
        "ui/astrology/aspectSextileEnabled"

    # QSettings default value for the aspect Sextile being enabled.
    aspectSextileEnabledDefValue = True
    
    # QSettings key for the aspect Sextile color.
    aspectSextileColorKey = \
        "ui/astrology/aspectSextileColor"

    # QSettings default value for the aspect Sextile color.
    aspectSextileColorDefValue = QColor(Qt.darkCyan)

    # QSettings key for the aspect Sextile orb in degrees.
    aspectSextileOrbKey = \
        "ui/astrology/aspectSextileOrb"

    # QSettings default value for the aspect Sextile orb in degrees (float).
    aspectSextileOrbDefValue = float(5.0)



    # QSettings key for the aspect Inconjunct name.
    aspectInconjunctNameKey = \
        "ui/astrology/aspectInconjunctName"

    # QSettings default value for the aspect Inconjunct name.
    aspectInconjunctNameDefValue = \
        "Inconjunct"
    
    # QSettings key for the aspect Inconjunct angle.
    aspectInconjunctAngleKey = \
        "ui/astrology/aspectInconjunctAngle"

    # QSettings default value for the aspect Inconjunct angle (float).
    aspectInconjunctAngleDefValue = float(150.0)
    
    # QSettings key for the aspect Inconjunct being enabled.
    aspectInconjunctEnabledKey = \
        "ui/astrology/aspectInconjunctEnabled"

    # QSettings default value for the aspect Inconjunct being enabled.
    aspectInconjunctEnabledDefValue = False
    
    # QSettings key for the aspect Inconjunct color.
    aspectInconjunctColorKey = \
        "ui/astrology/aspectInconjunctColor"

    # QSettings default value for the aspect Inconjunct color.
    aspectInconjunctColorDefValue = QColor(Qt.magenta)

    # QSettings key for the aspect Inconjunct orb in degrees.
    aspectInconjunctOrbKey = \
        "ui/astrology/aspectInconjunctOrb"

    # QSettings default value for the aspect Inconjunct orb in degrees (float).
    aspectInconjunctOrbDefValue = float(3.0)



    # QSettings key for the aspect Semisextile name.
    aspectSemisextileNameKey = \
        "ui/astrology/aspectSemisextileName"

    # QSettings default value for the aspect Semisextile name.
    aspectSemisextileNameDefValue = \
        "Semisextile"
    
    # QSettings key for the aspect Semisextile angle.
    aspectSemisextileAngleKey = \
        "ui/astrology/aspectSemisextileAngle"

    # QSettings default value for the aspect Semisextile angle (float).
    aspectSemisextileAngleDefValue = float(30.0)
    
    # QSettings key for the aspect Semisextile being enabled.
    aspectSemisextileEnabledKey = \
        "ui/astrology/aspectSemisextileEnabled"

    # QSettings default value for the aspect Semisextile being enabled.
    aspectSemisextileEnabledDefValue = False
    
    # QSettings key for the aspect Semisextile color.
    aspectSemisextileColorKey = \
        "ui/astrology/aspectSemisextileColor"

    # QSettings default value for the aspect Semisextile color.
    aspectSemisextileColorDefValue = QColor(Qt.magenta)

    # QSettings key for the aspect Semisextile orb in degrees.
    aspectSemisextileOrbKey = \
        "ui/astrology/aspectSemisextileOrb"

    # QSettings default value for the aspect Semisextile orb in degrees (float).
    aspectSemisextileOrbDefValue = float(3.0)



    # QSettings key for the aspect Semisquare name.
    aspectSemisquareNameKey = \
        "ui/astrology/aspectSemisquareName"

    # QSettings default value for the aspect Semisquare name.
    aspectSemisquareNameDefValue = \
        "Semisquare"
    
    # QSettings key for the aspect Semisquare angle.
    aspectSemisquareAngleKey = \
        "ui/astrology/aspectSemisquareAngle"

    # QSettings default value for the aspect Semisquare angle (float).
    aspectSemisquareAngleDefValue = float(45.0)
    
    # QSettings key for the aspect Semisquare being enabled.
    aspectSemisquareEnabledKey = \
        "ui/astrology/aspectSemisquareEnabled"

    # QSettings default value for the aspect Semisquare being enabled.
    aspectSemisquareEnabledDefValue = False
    
    # QSettings key for the aspect Semisquare color.
    aspectSemisquareColorKey = \
        "ui/astrology/aspectSemisquareColor"

    # QSettings default value for the aspect Semisquare color.
    aspectSemisquareColorDefValue = QColor(Qt.darkYellow)

    # QSettings key for the aspect Semisquare orb in degrees.
    aspectSemisquareOrbKey = \
        "ui/astrology/aspectSemisquareOrb"

    # QSettings default value for the aspect Semisquare orb in degrees (float).
    aspectSemisquareOrbDefValue = float(3.0)



    # QSettings key for the aspect Sesquiquadrate name.
    aspectSesquiquadrateNameKey = \
        "ui/astrology/aspectSesquiquadrateName"

    # QSettings default value for the aspect Sesquiquadrate name.
    aspectSesquiquadrateNameDefValue = \
        "Sesquiquadrate"
    
    # QSettings key for the aspect Sesquiquadrate angle.
    aspectSesquiquadrateAngleKey = \
        "ui/astrology/aspectSesquiquadrateAngle"

    # QSettings default value for the aspect Sesquiquadrate angle (float).
    aspectSesquiquadrateAngleDefValue = float(135.0)
    
    # QSettings key for the aspect Sesquiquadrate being enabled.
    aspectSesquiquadrateEnabledKey = \
        "ui/astrology/aspectSesquiquadrateEnabled"

    # QSettings default value for the aspect Sesquiquadrate being enabled.
    aspectSesquiquadrateEnabledDefValue = False
    
    # QSettings key for the aspect Sesquiquadrate color.
    aspectSesquiquadrateColorKey = \
        "ui/astrology/aspectSesquiquadrateColor"

    # QSettings default value for the aspect Sesquiquadrate color.
    aspectSesquiquadrateColorDefValue = QColor(Qt.darkYellow)

    # QSettings key for the aspect Sesquiquadrate orb in degrees.
    aspectSesquiquadrateOrbKey = \
        "ui/astrology/aspectSesquiquadrateOrb"

    # QSettings default value for the aspect Sesquiquadrate orb in degrees (float).
    aspectSesquiquadrateOrbDefValue = float(3.0)



    # QSettings key for enabled astrologychart calculations for H1.
    planetH1CalculationsEnabledKey = \
        "ui/astrology/h1CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H1.
    planetH1CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H2.
    planetH2CalculationsEnabledKey = \
        "ui/astrology/h2CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H2.
    planetH2CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H3.
    planetH3CalculationsEnabledKey = \
        "ui/astrology/h3CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H3.
    planetH3CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H4.
    planetH4CalculationsEnabledKey = \
        "ui/astrology/h4CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H4.
    planetH4CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H5.
    planetH5CalculationsEnabledKey = \
        "ui/astrology/h5CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H5.
    planetH5CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H6.
    planetH6CalculationsEnabledKey = \
        "ui/astrology/h6CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H6.
    planetH6CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H7.
    planetH7CalculationsEnabledKey = \
        "ui/astrology/h7CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H7.
    planetH7CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H8.
    planetH8CalculationsEnabledKey = \
        "ui/astrology/h8CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H8.
    planetH8CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H9.
    planetH9CalculationsEnabledKey = \
        "ui/astrology/h9CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H9.
    planetH9CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H10.
    planetH10CalculationsEnabledKey = \
        "ui/astrology/h10CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H10.
    planetH10CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H11.
    planetH11CalculationsEnabledKey = \
        "ui/astrology/h11CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H11.
    planetH11CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for H12.
    planetH12CalculationsEnabledKey = \
        "ui/astrology/h12CalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for H12.
    planetH12CalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for HoraLagna.
    planetHoraLagnaCalculationsEnabledKey = \
        "ui/astrology/horaLagnaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for HoraLagna.
    planetHoraLagnaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for GhatiLagna.
    planetGhatiLagnaCalculationsEnabledKey = \
        "ui/astrology/ghatiLagnaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for GhatiLagna.
    planetGhatiLagnaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeanLunarApogee.
    planetMeanLunarApogeeCalculationsEnabledKey = \
        "ui/astrology/meanLunarApogeeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeanLunarApogee.
    planetMeanLunarApogeeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for OsculatingLunarApogee.
    planetOsculatingLunarApogeeCalculationsEnabledKey = \
        "ui/astrology/osculatingLunarApogeeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for OsculatingLunarApogee.
    planetOsculatingLunarApogeeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeCalculationsEnabledKey = \
        "ui/astrology/interpolatedLunarApogeeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeCalculationsEnabledKey = \
        "ui/astrology/interpolatedLunarPerigeeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Sun.
    planetSunCalculationsEnabledKey = \
        "ui/astrology/sunCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Sun.
    planetSunCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Moon.
    planetMoonCalculationsEnabledKey = \
        "ui/astrology/moonCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Moon.
    planetMoonCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Mercury.
    planetMercuryCalculationsEnabledKey = \
        "ui/astrology/mercuryCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Mercury.
    planetMercuryCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Venus.
    planetVenusCalculationsEnabledKey = \
        "ui/astrology/venusCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Venus.
    planetVenusCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Earth.
    planetEarthCalculationsEnabledKey = \
        "ui/astrology/earthCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Earth.
    planetEarthCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Mars.
    planetMarsCalculationsEnabledKey = \
        "ui/astrology/marsCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Mars.
    planetMarsCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Jupiter.
    planetJupiterCalculationsEnabledKey = \
        "ui/astrology/jupiterCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Jupiter.
    planetJupiterCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Saturn.
    planetSaturnCalculationsEnabledKey = \
        "ui/astrology/saturnCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Saturn.
    planetSaturnCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Uranus.
    planetUranusCalculationsEnabledKey = \
        "ui/astrology/uranusCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Uranus.
    planetUranusCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Neptune.
    planetNeptuneCalculationsEnabledKey = \
        "ui/astrology/neptuneCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Neptune.
    planetNeptuneCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Pluto.
    planetPlutoCalculationsEnabledKey = \
        "ui/astrology/plutoCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Pluto.
    planetPlutoCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for MeanNorthNode.
    planetMeanNorthNodeCalculationsEnabledKey = \
        "ui/astrology/meanNorthNodeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeanNorthNode.
    planetMeanNorthNodeCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for MeanSouthNode.
    planetMeanSouthNodeCalculationsEnabledKey = \
        "ui/astrology/meanSouthNodeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeanSouthNode.
    planetMeanSouthNodeCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for TrueNorthNode.
    planetTrueNorthNodeCalculationsEnabledKey = \
        "ui/astrology/trueNorthNodeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for TrueNorthNode.
    planetTrueNorthNodeCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for TrueSouthNode.
    planetTrueSouthNodeCalculationsEnabledKey = \
        "ui/astrology/trueSouthNodeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for TrueSouthNode.
    planetTrueSouthNodeCalculationsEnabledDefValue = \
        True

    # QSettings key for enabled astrologychart calculations for Ceres.
    planetCeresCalculationsEnabledKey = \
        "ui/astrology/ceresCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Ceres.
    planetCeresCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Pallas.
    planetPallasCalculationsEnabledKey = \
        "ui/astrology/pallasCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Pallas.
    planetPallasCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Juno.
    planetJunoCalculationsEnabledKey = \
        "ui/astrology/junoCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Juno.
    planetJunoCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Vesta.
    planetVestaCalculationsEnabledKey = \
        "ui/astrology/vestaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Vesta.
    planetVestaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Isis.
    planetIsisCalculationsEnabledKey = \
        "ui/astrology/isisCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Isis.
    planetIsisCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Nibiru.
    planetNibiruCalculationsEnabledKey = \
        "ui/astrology/nibiruCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Nibiru.
    planetNibiruCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Chiron.
    planetChironCalculationsEnabledKey = \
        "ui/astrology/chironCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Chiron.
    planetChironCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Gulika.
    planetGulikaCalculationsEnabledKey = \
        "ui/astrology/gulikaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Gulika.
    planetGulikaCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for Mandi.
    planetMandiCalculationsEnabledKey = \
        "ui/astrology/mandiCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for Mandi.
    planetMandiCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for MeanOfFive.
    planetMeanOfFiveCalculationsEnabledKey = \
        "ui/astrology/meanOfFiveCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for MeanOfFive.
    planetMeanOfFiveCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for CycleOfEight.
    planetCycleOfEightCalculationsEnabledKey = \
        "ui/astrology/cycleOfEightCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for CycleOfEight.
    planetCycleOfEightCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlCalculationsEnabledKey = \
        "ui/astrology/avgMaJuSaUrNePlCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for AvgJuSaUrNe.
    planetAvgJuSaUrNeCalculationsEnabledKey = \
        "ui/astrology/avgJuSaUrNeCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for AvgJuSaUrNe.
    planetAvgJuSaUrNeCalculationsEnabledDefValue = \
        False

    # QSettings key for enabled astrologychart calculations for AvgJuSa.
    planetAvgJuSaCalculationsEnabledKey = \
        "ui/astrology/avgJuSaCalculationsEnabled"

    # QSettings default value for enabled astrologychart calculations for AvgJuSa.
    planetAvgJuSaCalculationsEnabledDefValue = \
        False



    # QSettings key for the display flag in PlanetaryInfoTable for H1.
    planetH1EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h1EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H1.
    planetH1EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H2.
    planetH2EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h2EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H2.
    planetH2EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H3.
    planetH3EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h3EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H3.
    planetH3EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H4.
    planetH4EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h4EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H4.
    planetH4EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H5.
    planetH5EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h5EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H5.
    planetH5EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H6.
    planetH6EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h6EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H6.
    planetH6EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H7.
    planetH7EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h7EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H7.
    planetH7EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H8.
    planetH8EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h8EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H8.
    planetH8EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H9.
    planetH9EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h9EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H9.
    planetH9EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H10.
    planetH10EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h10EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H10.
    planetH10EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H11.
    planetH11EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h11EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H11.
    planetH11EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for H12.
    planetH12EnabledForPlanetaryInfoTableKey = \
        "ui/astrology/h12EnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for H12.
    planetH12EnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for HoraLagna.
    planetHoraLagnaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/horaLagnaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for HoraLagna.
    planetHoraLagnaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for GhatiLagna.
    planetGhatiLagnaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/ghatiLagnaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for GhatiLagna.
    planetGhatiLagnaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/meanLunarApogeeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/osculatingLunarApogeeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/interpolatedLunarApogeeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/interpolatedLunarPerigeeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Sun.
    planetSunEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/sunEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Sun.
    planetSunEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Moon.
    planetMoonEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/moonEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Moon.
    planetMoonEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Mercury.
    planetMercuryEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/mercuryEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Mercury.
    planetMercuryEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Venus.
    planetVenusEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/venusEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Venus.
    planetVenusEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Earth.
    planetEarthEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/earthEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Earth.
    planetEarthEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Mars.
    planetMarsEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/marsEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Mars.
    planetMarsEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Jupiter.
    planetJupiterEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/jupiterEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Jupiter.
    planetJupiterEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Saturn.
    planetSaturnEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/saturnEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Saturn.
    planetSaturnEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Uranus.
    planetUranusEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/uranusEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Uranus.
    planetUranusEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Neptune.
    planetNeptuneEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/neptuneEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Neptune.
    planetNeptuneEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Pluto.
    planetPlutoEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/plutoEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Pluto.
    planetPlutoEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeanNorthNode.
    planetMeanNorthNodeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/meanNorthNodeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeanNorthNode.
    planetMeanNorthNodeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeanSouthNode.
    planetMeanSouthNodeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/meanSouthNodeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeanSouthNode.
    planetMeanSouthNodeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for TrueNorthNode.
    planetTrueNorthNodeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/trueNorthNodeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for TrueNorthNode.
    planetTrueNorthNodeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for TrueSouthNode.
    planetTrueSouthNodeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/trueSouthNodeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for TrueSouthNode.
    planetTrueSouthNodeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for Ceres.
    planetCeresEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/ceresEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Ceres.
    planetCeresEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Pallas.
    planetPallasEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/pallasEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Pallas.
    planetPallasEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Juno.
    planetJunoEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/junoEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Juno.
    planetJunoEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Vesta.
    planetVestaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/vestaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Vesta.
    planetVestaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Isis.
    planetIsisEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/isisEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Isis.
    planetIsisEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Nibiru.
    planetNibiruEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/nibiruEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Nibiru.
    planetNibiruEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Chiron.
    planetChironEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/chironEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Chiron.
    planetChironEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Gulika.
    planetGulikaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/gulikaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Gulika.
    planetGulikaEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for Mandi.
    planetMandiEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/mandiEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for Mandi.
    planetMandiEnabledForPlanetaryInfoTableDefValue = \
        False
    
    # QSettings key for the display flag in PlanetaryInfoTable for MeanOfFive.
    planetMeanOfFiveEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/meanOfFiveEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for MeanOfFive.
    planetMeanOfFiveEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for CycleOfEight.
    planetCycleOfEightEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/cycleOfEightEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for CycleOfEight.
    planetCycleOfEightEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/avgMaJuSaUrNePlEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/avgJuSaUrNeEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForPlanetaryInfoTableDefValue = \
        True
    
    # QSettings key for the display flag in PlanetaryInfoTable for AvgJuSa.
    planetAvgJuSaEnabledForPlanetaryInfoTableKey = \
        "ui/astrology/avgJuSaEnabledForPlanetaryInfoTable"
    
    # QSettings default value for the display flag in PlanetaryInfoTable for AvgJuSa.
    planetAvgJuSaEnabledForPlanetaryInfoTableDefValue = \
        True
    
    
    
    # QSettings key for the display flag in Declination for H1.
    planetH1EnabledForDeclinationKey = \
        "ui/astrology/h1EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H1.
    planetH1EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H2.
    planetH2EnabledForDeclinationKey = \
        "ui/astrology/h2EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H2.
    planetH2EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H3.
    planetH3EnabledForDeclinationKey = \
        "ui/astrology/h3EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H3.
    planetH3EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H4.
    planetH4EnabledForDeclinationKey = \
        "ui/astrology/h4EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H4.
    planetH4EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H5.
    planetH5EnabledForDeclinationKey = \
        "ui/astrology/h5EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H5.
    planetH5EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H6.
    planetH6EnabledForDeclinationKey = \
        "ui/astrology/h6EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H6.
    planetH6EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H7.
    planetH7EnabledForDeclinationKey = \
        "ui/astrology/h7EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H7.
    planetH7EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H8.
    planetH8EnabledForDeclinationKey = \
        "ui/astrology/h8EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H8.
    planetH8EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H9.
    planetH9EnabledForDeclinationKey = \
        "ui/astrology/h9EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H9.
    planetH9EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H10.
    planetH10EnabledForDeclinationKey = \
        "ui/astrology/h10EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H10.
    planetH10EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H11.
    planetH11EnabledForDeclinationKey = \
        "ui/astrology/h11EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H11.
    planetH11EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for H12.
    planetH12EnabledForDeclinationKey = \
        "ui/astrology/h12EnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for H12.
    planetH12EnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for HoraLagna.
    planetHoraLagnaEnabledForDeclinationKey = \
        "ui/astrology/horaLagnaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for HoraLagna.
    planetHoraLagnaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for GhatiLagna.
    planetGhatiLagnaEnabledForDeclinationKey = \
        "ui/astrology/ghatiLagnaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for GhatiLagna.
    planetGhatiLagnaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForDeclinationKey = \
        "ui/astrology/meanLunarApogeeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForDeclinationKey = \
        "ui/astrology/osculatingLunarApogeeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForDeclinationKey = \
        "ui/astrology/interpolatedLunarApogeeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForDeclinationKey = \
        "ui/astrology/interpolatedLunarPerigeeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Sun.
    planetSunEnabledForDeclinationKey = \
        "ui/astrology/sunEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Sun.
    planetSunEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Moon.
    planetMoonEnabledForDeclinationKey = \
        "ui/astrology/moonEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Moon.
    planetMoonEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Mercury.
    planetMercuryEnabledForDeclinationKey = \
        "ui/astrology/mercuryEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Mercury.
    planetMercuryEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Venus.
    planetVenusEnabledForDeclinationKey = \
        "ui/astrology/venusEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Venus.
    planetVenusEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Earth.
    planetEarthEnabledForDeclinationKey = \
        "ui/astrology/earthEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Earth.
    planetEarthEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Mars.
    planetMarsEnabledForDeclinationKey = \
        "ui/astrology/marsEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Mars.
    planetMarsEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Jupiter.
    planetJupiterEnabledForDeclinationKey = \
        "ui/astrology/jupiterEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Jupiter.
    planetJupiterEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Saturn.
    planetSaturnEnabledForDeclinationKey = \
        "ui/astrology/saturnEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Saturn.
    planetSaturnEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Uranus.
    planetUranusEnabledForDeclinationKey = \
        "ui/astrology/uranusEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Uranus.
    planetUranusEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Neptune.
    planetNeptuneEnabledForDeclinationKey = \
        "ui/astrology/neptuneEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Neptune.
    planetNeptuneEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for Pluto.
    planetPlutoEnabledForDeclinationKey = \
        "ui/astrology/plutoEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Pluto.
    planetPlutoEnabledForDeclinationDefValue = \
        True
    
    # QSettings key for the display flag in Declination for MeanNorthNode.
    planetMeanNorthNodeEnabledForDeclinationKey = \
        "ui/astrology/meanNorthNodeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeanNorthNode.
    planetMeanNorthNodeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeanSouthNode.
    planetMeanSouthNodeEnabledForDeclinationKey = \
        "ui/astrology/meanSouthNodeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeanSouthNode.
    planetMeanSouthNodeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for TrueNorthNode.
    planetTrueNorthNodeEnabledForDeclinationKey = \
        "ui/astrology/trueNorthNodeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for TrueNorthNode.
    planetTrueNorthNodeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for TrueSouthNode.
    planetTrueSouthNodeEnabledForDeclinationKey = \
        "ui/astrology/trueSouthNodeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for TrueSouthNode.
    planetTrueSouthNodeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Ceres.
    planetCeresEnabledForDeclinationKey = \
        "ui/astrology/ceresEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Ceres.
    planetCeresEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Pallas.
    planetPallasEnabledForDeclinationKey = \
        "ui/astrology/pallasEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Pallas.
    planetPallasEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Juno.
    planetJunoEnabledForDeclinationKey = \
        "ui/astrology/junoEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Juno.
    planetJunoEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Vesta.
    planetVestaEnabledForDeclinationKey = \
        "ui/astrology/vestaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Vesta.
    planetVestaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Isis.
    planetIsisEnabledForDeclinationKey = \
        "ui/astrology/isisEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Isis.
    planetIsisEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Nibiru.
    planetNibiruEnabledForDeclinationKey = \
        "ui/astrology/nibiruEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Nibiru.
    planetNibiruEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Chiron.
    planetChironEnabledForDeclinationKey = \
        "ui/astrology/chironEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Chiron.
    planetChironEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Gulika.
    planetGulikaEnabledForDeclinationKey = \
        "ui/astrology/gulikaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Gulika.
    planetGulikaEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for Mandi.
    planetMandiEnabledForDeclinationKey = \
        "ui/astrology/mandiEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for Mandi.
    planetMandiEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for MeanOfFive.
    planetMeanOfFiveEnabledForDeclinationKey = \
        "ui/astrology/meanOfFiveEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for MeanOfFive.
    planetMeanOfFiveEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for CycleOfEight.
    planetCycleOfEightEnabledForDeclinationKey = \
        "ui/astrology/cycleOfEightEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for CycleOfEight.
    planetCycleOfEightEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForDeclinationKey = \
        "ui/astrology/avgMaJuSaUrNePlEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForDeclinationKey = \
        "ui/astrology/avgJuSaUrNeEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForDeclinationDefValue = \
        False
    
    # QSettings key for the display flag in Declination for AvgJuSa.
    planetAvgJuSaEnabledForDeclinationKey = \
        "ui/astrology/avgJuSaEnabledForDeclination"
    
    # QSettings default value for the display flag in Declination for AvgJuSa.
    planetAvgJuSaEnabledForDeclinationDefValue = \
        False
    


    # QSettings key for the display flag in Latitude for H1.
    planetH1EnabledForLatitudeKey = \
        "ui/astrology/h1EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H1.
    planetH1EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H2.
    planetH2EnabledForLatitudeKey = \
        "ui/astrology/h2EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H2.
    planetH2EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H3.
    planetH3EnabledForLatitudeKey = \
        "ui/astrology/h3EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H3.
    planetH3EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H4.
    planetH4EnabledForLatitudeKey = \
        "ui/astrology/h4EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H4.
    planetH4EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H5.
    planetH5EnabledForLatitudeKey = \
        "ui/astrology/h5EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H5.
    planetH5EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H6.
    planetH6EnabledForLatitudeKey = \
        "ui/astrology/h6EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H6.
    planetH6EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H7.
    planetH7EnabledForLatitudeKey = \
        "ui/astrology/h7EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H7.
    planetH7EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H8.
    planetH8EnabledForLatitudeKey = \
        "ui/astrology/h8EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H8.
    planetH8EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H9.
    planetH9EnabledForLatitudeKey = \
        "ui/astrology/h9EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H9.
    planetH9EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H10.
    planetH10EnabledForLatitudeKey = \
        "ui/astrology/h10EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H10.
    planetH10EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H11.
    planetH11EnabledForLatitudeKey = \
        "ui/astrology/h11EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H11.
    planetH11EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for H12.
    planetH12EnabledForLatitudeKey = \
        "ui/astrology/h12EnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for H12.
    planetH12EnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for HoraLagna.
    planetHoraLagnaEnabledForLatitudeKey = \
        "ui/astrology/horaLagnaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for HoraLagna.
    planetHoraLagnaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for GhatiLagna.
    planetGhatiLagnaEnabledForLatitudeKey = \
        "ui/astrology/ghatiLagnaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for GhatiLagna.
    planetGhatiLagnaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForLatitudeKey = \
        "ui/astrology/meanLunarApogeeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForLatitudeKey = \
        "ui/astrology/osculatingLunarApogeeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForLatitudeKey = \
        "ui/astrology/interpolatedLunarApogeeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForLatitudeKey = \
        "ui/astrology/interpolatedLunarPerigeeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Sun.
    planetSunEnabledForLatitudeKey = \
        "ui/astrology/sunEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Sun.
    planetSunEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Moon.
    planetMoonEnabledForLatitudeKey = \
        "ui/astrology/moonEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Moon.
    planetMoonEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Mercury.
    planetMercuryEnabledForLatitudeKey = \
        "ui/astrology/mercuryEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Mercury.
    planetMercuryEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Venus.
    planetVenusEnabledForLatitudeKey = \
        "ui/astrology/venusEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Venus.
    planetVenusEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Earth.
    planetEarthEnabledForLatitudeKey = \
        "ui/astrology/earthEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Earth.
    planetEarthEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Mars.
    planetMarsEnabledForLatitudeKey = \
        "ui/astrology/marsEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Mars.
    planetMarsEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Jupiter.
    planetJupiterEnabledForLatitudeKey = \
        "ui/astrology/jupiterEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Jupiter.
    planetJupiterEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Saturn.
    planetSaturnEnabledForLatitudeKey = \
        "ui/astrology/saturnEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Saturn.
    planetSaturnEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Uranus.
    planetUranusEnabledForLatitudeKey = \
        "ui/astrology/uranusEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Uranus.
    planetUranusEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Neptune.
    planetNeptuneEnabledForLatitudeKey = \
        "ui/astrology/neptuneEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Neptune.
    planetNeptuneEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for Pluto.
    planetPlutoEnabledForLatitudeKey = \
        "ui/astrology/plutoEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Pluto.
    planetPlutoEnabledForLatitudeDefValue = \
        True
    
    # QSettings key for the display flag in Latitude for MeanNorthNode.
    planetMeanNorthNodeEnabledForLatitudeKey = \
        "ui/astrology/meanNorthNodeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeanNorthNode.
    planetMeanNorthNodeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeanSouthNode.
    planetMeanSouthNodeEnabledForLatitudeKey = \
        "ui/astrology/meanSouthNodeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeanSouthNode.
    planetMeanSouthNodeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for TrueNorthNode.
    planetTrueNorthNodeEnabledForLatitudeKey = \
        "ui/astrology/trueNorthNodeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for TrueNorthNode.
    planetTrueNorthNodeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for TrueSouthNode.
    planetTrueSouthNodeEnabledForLatitudeKey = \
        "ui/astrology/trueSouthNodeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for TrueSouthNode.
    planetTrueSouthNodeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Ceres.
    planetCeresEnabledForLatitudeKey = \
        "ui/astrology/ceresEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Ceres.
    planetCeresEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Pallas.
    planetPallasEnabledForLatitudeKey = \
        "ui/astrology/pallasEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Pallas.
    planetPallasEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Juno.
    planetJunoEnabledForLatitudeKey = \
        "ui/astrology/junoEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Juno.
    planetJunoEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Vesta.
    planetVestaEnabledForLatitudeKey = \
        "ui/astrology/vestaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Vesta.
    planetVestaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Isis.
    planetIsisEnabledForLatitudeKey = \
        "ui/astrology/isisEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Isis.
    planetIsisEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Nibiru.
    planetNibiruEnabledForLatitudeKey = \
        "ui/astrology/nibiruEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Nibiru.
    planetNibiruEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Chiron.
    planetChironEnabledForLatitudeKey = \
        "ui/astrology/chironEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Chiron.
    planetChironEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Gulika.
    planetGulikaEnabledForLatitudeKey = \
        "ui/astrology/gulikaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Gulika.
    planetGulikaEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for Mandi.
    planetMandiEnabledForLatitudeKey = \
        "ui/astrology/mandiEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for Mandi.
    planetMandiEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for MeanOfFive.
    planetMeanOfFiveEnabledForLatitudeKey = \
        "ui/astrology/meanOfFiveEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for MeanOfFive.
    planetMeanOfFiveEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for CycleOfEight.
    planetCycleOfEightEnabledForLatitudeKey = \
        "ui/astrology/cycleOfEightEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for CycleOfEight.
    planetCycleOfEightEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForLatitudeKey = \
        "ui/astrology/avgMaJuSaUrNePlEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForLatitudeKey = \
        "ui/astrology/avgJuSaUrNeEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForLatitudeDefValue = \
        False
    
    # QSettings key for the display flag in Latitude for AvgJuSa.
    planetAvgJuSaEnabledForLatitudeKey = \
        "ui/astrology/avgJuSaEnabledForLatitude"
    
    # QSettings default value for the display flag in Latitude for AvgJuSa.
    planetAvgJuSaEnabledForLatitudeDefValue = \
        False
    

    
    # QSettings key for the display flag in GeoSidRadixChart for H1.
    planetH1EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h1EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H1.
    planetH1EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H2.
    planetH2EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h2EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H2.
    planetH2EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H3.
    planetH3EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h3EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H3.
    planetH3EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H4.
    planetH4EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h4EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H4.
    planetH4EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H5.
    planetH5EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h5EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H5.
    planetH5EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H6.
    planetH6EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h6EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H6.
    planetH6EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H7.
    planetH7EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h7EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H7.
    planetH7EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H8.
    planetH8EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h8EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H8.
    planetH8EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H9.
    planetH9EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h9EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H9.
    planetH9EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H10.
    planetH10EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h10EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H10.
    planetH10EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H11.
    planetH11EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h11EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H11.
    planetH11EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for H12.
    planetH12EnabledForGeoSidRadixChartKey = \
        "ui/astrology/h12EnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for H12.
    planetH12EnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for HoraLagna.
    planetHoraLagnaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/horaLagnaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for HoraLagna.
    planetHoraLagnaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/ghatiLagnaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/meanLunarApogeeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/osculatingLunarApogeeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/interpolatedLunarApogeeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/interpolatedLunarPerigeeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Sun.
    planetSunEnabledForGeoSidRadixChartKey = \
        "ui/astrology/sunEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Sun.
    planetSunEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Moon.
    planetMoonEnabledForGeoSidRadixChartKey = \
        "ui/astrology/moonEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Moon.
    planetMoonEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Mercury.
    planetMercuryEnabledForGeoSidRadixChartKey = \
        "ui/astrology/mercuryEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Mercury.
    planetMercuryEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Venus.
    planetVenusEnabledForGeoSidRadixChartKey = \
        "ui/astrology/venusEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Venus.
    planetVenusEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Earth.
    planetEarthEnabledForGeoSidRadixChartKey = \
        "ui/astrology/earthEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Earth.
    planetEarthEnabledForGeoSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoSidRadixChart for Mars.
    planetMarsEnabledForGeoSidRadixChartKey = \
        "ui/astrology/marsEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Mars.
    planetMarsEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Jupiter.
    planetJupiterEnabledForGeoSidRadixChartKey = \
        "ui/astrology/jupiterEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Jupiter.
    planetJupiterEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Saturn.
    planetSaturnEnabledForGeoSidRadixChartKey = \
        "ui/astrology/saturnEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Saturn.
    planetSaturnEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Uranus.
    planetUranusEnabledForGeoSidRadixChartKey = \
        "ui/astrology/uranusEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Uranus.
    planetUranusEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Neptune.
    planetNeptuneEnabledForGeoSidRadixChartKey = \
        "ui/astrology/neptuneEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Neptune.
    planetNeptuneEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Pluto.
    planetPlutoEnabledForGeoSidRadixChartKey = \
        "ui/astrology/plutoEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Pluto.
    planetPlutoEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/meanNorthNodeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/meanSouthNodeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/trueNorthNodeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/trueSouthNodeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Ceres.
    planetCeresEnabledForGeoSidRadixChartKey = \
        "ui/astrology/ceresEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Ceres.
    planetCeresEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Pallas.
    planetPallasEnabledForGeoSidRadixChartKey = \
        "ui/astrology/pallasEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Pallas.
    planetPallasEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Juno.
    planetJunoEnabledForGeoSidRadixChartKey = \
        "ui/astrology/junoEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Juno.
    planetJunoEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Vesta.
    planetVestaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/vestaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Vesta.
    planetVestaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Isis.
    planetIsisEnabledForGeoSidRadixChartKey = \
        "ui/astrology/isisEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Isis.
    planetIsisEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Nibiru.
    planetNibiruEnabledForGeoSidRadixChartKey = \
        "ui/astrology/nibiruEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Nibiru.
    planetNibiruEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Chiron.
    planetChironEnabledForGeoSidRadixChartKey = \
        "ui/astrology/chironEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Chiron.
    planetChironEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Gulika.
    planetGulikaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/gulikaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Gulika.
    planetGulikaEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for Mandi.
    planetMandiEnabledForGeoSidRadixChartKey = \
        "ui/astrology/mandiEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for Mandi.
    planetMandiEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForGeoSidRadixChartKey = \
        "ui/astrology/meanOfFiveEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForGeoSidRadixChartKey = \
        "ui/astrology/cycleOfEightEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForGeoSidRadixChartKey = \
        "ui/astrology/avgMaJuSaUrNePlEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForGeoSidRadixChartKey = \
        "ui/astrology/avgJuSaUrNeEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForGeoSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoSidRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForGeoSidRadixChartKey = \
        "ui/astrology/avgJuSaEnabledForGeoSidRadixChart"
    
    # QSettings default value for the display flag in GeoSidRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForGeoSidRadixChartDefValue = \
        True
    

    
    # QSettings key for the display flag in GeoTropRadixChart for H1.
    planetH1EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h1EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H1.
    planetH1EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H2.
    planetH2EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h2EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H2.
    planetH2EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H3.
    planetH3EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h3EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H3.
    planetH3EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H4.
    planetH4EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h4EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H4.
    planetH4EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H5.
    planetH5EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h5EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H5.
    planetH5EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H6.
    planetH6EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h6EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H6.
    planetH6EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H7.
    planetH7EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h7EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H7.
    planetH7EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H8.
    planetH8EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h8EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H8.
    planetH8EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H9.
    planetH9EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h9EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H9.
    planetH9EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H10.
    planetH10EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h10EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H10.
    planetH10EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H11.
    planetH11EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h11EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H11.
    planetH11EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for H12.
    planetH12EnabledForGeoTropRadixChartKey = \
        "ui/astrology/h12EnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for H12.
    planetH12EnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for HoraLagna.
    planetHoraLagnaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/horaLagnaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for HoraLagna.
    planetHoraLagnaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/ghatiLagnaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/meanLunarApogeeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/osculatingLunarApogeeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/interpolatedLunarApogeeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/interpolatedLunarPerigeeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Sun.
    planetSunEnabledForGeoTropRadixChartKey = \
        "ui/astrology/sunEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Sun.
    planetSunEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Moon.
    planetMoonEnabledForGeoTropRadixChartKey = \
        "ui/astrology/moonEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Moon.
    planetMoonEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Mercury.
    planetMercuryEnabledForGeoTropRadixChartKey = \
        "ui/astrology/mercuryEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Mercury.
    planetMercuryEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Venus.
    planetVenusEnabledForGeoTropRadixChartKey = \
        "ui/astrology/venusEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Venus.
    planetVenusEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Earth.
    planetEarthEnabledForGeoTropRadixChartKey = \
        "ui/astrology/earthEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Earth.
    planetEarthEnabledForGeoTropRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in GeoTropRadixChart for Mars.
    planetMarsEnabledForGeoTropRadixChartKey = \
        "ui/astrology/marsEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Mars.
    planetMarsEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Jupiter.
    planetJupiterEnabledForGeoTropRadixChartKey = \
        "ui/astrology/jupiterEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Jupiter.
    planetJupiterEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Saturn.
    planetSaturnEnabledForGeoTropRadixChartKey = \
        "ui/astrology/saturnEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Saturn.
    planetSaturnEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Uranus.
    planetUranusEnabledForGeoTropRadixChartKey = \
        "ui/astrology/uranusEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Uranus.
    planetUranusEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Neptune.
    planetNeptuneEnabledForGeoTropRadixChartKey = \
        "ui/astrology/neptuneEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Neptune.
    planetNeptuneEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Pluto.
    planetPlutoEnabledForGeoTropRadixChartKey = \
        "ui/astrology/plutoEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Pluto.
    planetPlutoEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/meanNorthNodeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/meanSouthNodeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/trueNorthNodeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/trueSouthNodeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Ceres.
    planetCeresEnabledForGeoTropRadixChartKey = \
        "ui/astrology/ceresEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Ceres.
    planetCeresEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Pallas.
    planetPallasEnabledForGeoTropRadixChartKey = \
        "ui/astrology/pallasEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Pallas.
    planetPallasEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Juno.
    planetJunoEnabledForGeoTropRadixChartKey = \
        "ui/astrology/junoEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Juno.
    planetJunoEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Vesta.
    planetVestaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/vestaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Vesta.
    planetVestaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Isis.
    planetIsisEnabledForGeoTropRadixChartKey = \
        "ui/astrology/isisEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Isis.
    planetIsisEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Nibiru.
    planetNibiruEnabledForGeoTropRadixChartKey = \
        "ui/astrology/nibiruEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Nibiru.
    planetNibiruEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Chiron.
    planetChironEnabledForGeoTropRadixChartKey = \
        "ui/astrology/chironEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Chiron.
    planetChironEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Gulika.
    planetGulikaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/gulikaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Gulika.
    planetGulikaEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for Mandi.
    planetMandiEnabledForGeoTropRadixChartKey = \
        "ui/astrology/mandiEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for Mandi.
    planetMandiEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForGeoTropRadixChartKey = \
        "ui/astrology/meanOfFiveEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForGeoTropRadixChartKey = \
        "ui/astrology/cycleOfEightEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForGeoTropRadixChartKey = \
        "ui/astrology/avgMaJuSaUrNePlEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForGeoTropRadixChartKey = \
        "ui/astrology/avgJuSaUrNeEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForGeoTropRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in GeoTropRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForGeoTropRadixChartKey = \
        "ui/astrology/avgJuSaEnabledForGeoTropRadixChart"
    
    # QSettings default value for the display flag in GeoTropRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForGeoTropRadixChartDefValue = \
        True
    

    
    # QSettings key for the display flag in HelioSidRadixChart for H1.
    planetH1EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h1EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H1.
    planetH1EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H2.
    planetH2EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h2EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H2.
    planetH2EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H3.
    planetH3EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h3EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H3.
    planetH3EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H4.
    planetH4EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h4EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H4.
    planetH4EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H5.
    planetH5EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h5EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H5.
    planetH5EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H6.
    planetH6EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h6EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H6.
    planetH6EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H7.
    planetH7EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h7EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H7.
    planetH7EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H8.
    planetH8EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h8EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H8.
    planetH8EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H9.
    planetH9EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h9EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H9.
    planetH9EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H10.
    planetH10EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h10EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H10.
    planetH10EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H11.
    planetH11EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h11EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H11.
    planetH11EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for H12.
    planetH12EnabledForHelioSidRadixChartKey = \
        "ui/astrology/h12EnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for H12.
    planetH12EnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for HoraLagna.
    planetHoraLagnaEnabledForHelioSidRadixChartKey = \
        "ui/astrology/horaLagnaEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for HoraLagna.
    planetHoraLagnaEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForHelioSidRadixChartKey = \
        "ui/astrology/ghatiLagnaEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for GhatiLagna.
    planetGhatiLagnaEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/meanLunarApogeeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for MeanLunarApogee.
    planetMeanLunarApogeeEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/osculatingLunarApogeeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for OsculatingLunarApogee.
    planetOsculatingLunarApogeeEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/interpolatedLunarApogeeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for InterpolatedLunarApogee.
    planetInterpolatedLunarApogeeEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/interpolatedLunarPerigeeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for InterpolatedLunarPerigee.
    planetInterpolatedLunarPerigeeEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Sun.
    planetSunEnabledForHelioSidRadixChartKey = \
        "ui/astrology/sunEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Sun.
    planetSunEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Moon.
    planetMoonEnabledForHelioSidRadixChartKey = \
        "ui/astrology/moonEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Moon.
    planetMoonEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Mercury.
    planetMercuryEnabledForHelioSidRadixChartKey = \
        "ui/astrology/mercuryEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Mercury.
    planetMercuryEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for Venus.
    planetVenusEnabledForHelioSidRadixChartKey = \
        "ui/astrology/venusEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Venus.
    planetVenusEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for Earth.
    planetEarthEnabledForHelioSidRadixChartKey = \
        "ui/astrology/earthEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Earth.
    planetEarthEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for Mars.
    planetMarsEnabledForHelioSidRadixChartKey = \
        "ui/astrology/marsEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Mars.
    planetMarsEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for Jupiter.
    planetJupiterEnabledForHelioSidRadixChartKey = \
        "ui/astrology/jupiterEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Jupiter.
    planetJupiterEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for Saturn.
    planetSaturnEnabledForHelioSidRadixChartKey = \
        "ui/astrology/saturnEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Saturn.
    planetSaturnEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for Uranus.
    planetUranusEnabledForHelioSidRadixChartKey = \
        "ui/astrology/uranusEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Uranus.
    planetUranusEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for Neptune.
    planetNeptuneEnabledForHelioSidRadixChartKey = \
        "ui/astrology/neptuneEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Neptune.
    planetNeptuneEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for Pluto.
    planetPlutoEnabledForHelioSidRadixChartKey = \
        "ui/astrology/plutoEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Pluto.
    planetPlutoEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/meanNorthNodeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for MeanNorthNode.
    planetMeanNorthNodeEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/meanSouthNodeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for MeanSouthNode.
    planetMeanSouthNodeEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/trueNorthNodeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for TrueNorthNode.
    planetTrueNorthNodeEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/trueSouthNodeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for TrueSouthNode.
    planetTrueSouthNodeEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Ceres.
    planetCeresEnabledForHelioSidRadixChartKey = \
        "ui/astrology/ceresEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Ceres.
    planetCeresEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Pallas.
    planetPallasEnabledForHelioSidRadixChartKey = \
        "ui/astrology/pallasEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Pallas.
    planetPallasEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Juno.
    planetJunoEnabledForHelioSidRadixChartKey = \
        "ui/astrology/junoEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Juno.
    planetJunoEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Vesta.
    planetVestaEnabledForHelioSidRadixChartKey = \
        "ui/astrology/vestaEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Vesta.
    planetVestaEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Isis.
    planetIsisEnabledForHelioSidRadixChartKey = \
        "ui/astrology/isisEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Isis.
    planetIsisEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Nibiru.
    planetNibiruEnabledForHelioSidRadixChartKey = \
        "ui/astrology/nibiruEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Nibiru.
    planetNibiruEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Chiron.
    planetChironEnabledForHelioSidRadixChartKey = \
        "ui/astrology/chironEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Chiron.
    planetChironEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Gulika.
    planetGulikaEnabledForHelioSidRadixChartKey = \
        "ui/astrology/gulikaEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Gulika.
    planetGulikaEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for Mandi.
    planetMandiEnabledForHelioSidRadixChartKey = \
        "ui/astrology/mandiEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for Mandi.
    planetMandiEnabledForHelioSidRadixChartDefValue = \
        False
    
    # QSettings key for the display flag in HelioSidRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForHelioSidRadixChartKey = \
        "ui/astrology/meanOfFiveEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for MeanOfFive.
    planetMeanOfFiveEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForHelioSidRadixChartKey = \
        "ui/astrology/cycleOfEightEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for CycleOfEight.
    planetCycleOfEightEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForHelioSidRadixChartKey = \
        "ui/astrology/avgMaJuSaUrNePlEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for AvgMaJuSaUrNePl.
    planetAvgMaJuSaUrNePlEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForHelioSidRadixChartKey = \
        "ui/astrology/avgJuSaUrNeEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for AvgJuSaUrNe.
    planetAvgJuSaUrNeEnabledForHelioSidRadixChartDefValue = \
        True
    
    # QSettings key for the display flag in HelioSidRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForHelioSidRadixChartKey = \
        "ui/astrology/avgJuSaEnabledForHelioSidRadixChart"
    
    # QSettings default value for the display flag in HelioSidRadixChart for AvgJuSa.
    planetAvgJuSaEnabledForHelioSidRadixChartDefValue = \
        True
    

    
