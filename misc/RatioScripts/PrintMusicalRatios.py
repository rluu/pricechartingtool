#!/usr/bin/env python3
##############################################################################
# File: PrintMusicalRatios.py
#
# Author:  Ryan Luu     ryanluu@gmail.com
#
# Description:
#    Prints the mathematical intervals for musical notes.
#
# Usage:
#   ./PrintMusicalRatios.py --help
#
#   ./PrintMusicalRatios.py --JustIntonationIntervals
#   ./PrintMusicalRatios.py --JustIntonationIntervalsInverted
#   ./PrintMusicalRatios.py --PythagoreanIntervals
#   ./PrintMusicalRatios.py --PythagoreanIntervalsInverted
#
#
##############################################################################


##############################################################################

# For calling sys.exit(1), etc.
import sys 

# For parsing command-line options
from optparse import OptionParser  

##############################################################################

# Version string.
VERSION = "0.1"

global options
global musicalRatios
musicalRatios = list()

class Number:
    def __init__(self, value=0.0, description=""):
        self.description = description
        self.value = value

    def toString(self):
        return "{},{}".format(self.description, self.value)

##############################################################################

##############################################################################

    
def findJustIntonationIntervalsInverted():
    global musicalRatios
    
    value = 1 / 1
    value = 1 / value
    valueDesc = "JI_Unison_Inverted(1/1)"
    musicalRatios.append(Number(value, valueDesc))

    value = 9 / 8
    value = 1 / value
    valueDesc = "JI_Major2nd_Inverted(8/9)"
    musicalRatios.append(Number(value, valueDesc))

    value = 5 / 4
    value = 1 / value
    valueDesc = "JI_Major3rd_Inverted(4/5)"
    musicalRatios.append(Number(value, valueDesc))

    value = 4 / 3
    value = 1 / value
    valueDesc = "JI_Perfect4th_Inverted(3/4)"
    musicalRatios.append(Number(value, valueDesc))

    value = 3 / 2
    value = 1 / value
    valueDesc = "JI_Perfect5th_Inverted(2/3)"
    musicalRatios.append(Number(value, valueDesc))

    value = 5 / 3
    value = 1 / value
    valueDesc = "JI_Major6th_Inverted(3/5)"
    musicalRatios.append(Number(value, valueDesc))

    value = 15 / 8
    value = 1 / value
    valueDesc = "JI_Major7th_Inverted(8/15)"
    musicalRatios.append(Number(value, valueDesc))

    value = 2 / 1
    value = 1 / value
    valueDesc = "JI_Octave_Inverted(1/2)"
    musicalRatios.append(Number(value, valueDesc))
    
def findJustIntonationIntervals():
    global musicalRatios
    
    value = 1 / 1
    valueDesc = "JI_Unison(1/1)"
    musicalRatios.append(Number(value, valueDesc))

    value = 9 / 8
    valueDesc = "JI_Major2nd(9/8)"
    musicalRatios.append(Number(value, valueDesc))

    value = 5 / 4
    valueDesc = "JI_Major3rd(5/4)"
    musicalRatios.append(Number(value, valueDesc))

    value = 4 / 3
    valueDesc = "JI_Perfect4th(4/3)"
    musicalRatios.append(Number(value, valueDesc))

    value = 3 / 2
    valueDesc = "JI_Perfect5th(3/2)"
    musicalRatios.append(Number(value, valueDesc))

    value = 5 / 3
    valueDesc = "JI_Major6th(5/3)"
    musicalRatios.append(Number(value, valueDesc))

    value = 15 / 8
    valueDesc = "JI_Major7th(15/8)"
    musicalRatios.append(Number(value, valueDesc))

    value = 2 / 1
    valueDesc = "JI_Octave(2/1)"
    musicalRatios.append(Number(value, valueDesc))

    
def findPythagoreanIntervalsInverted():
    global musicalRatios
    
    value = 1024 / 729
    value = 1 / value
    valueDesc = "PythagoreanDiminished5th_Inverted(729/1024)"
    musicalRatios.append(Number(value, valueDesc))

    value = 256 / 243
    value = 1 / value
    valueDesc = "PythagoreanMinor2nd_Inverted(243/256)"
    musicalRatios.append(Number(value, valueDesc))

    value = 128 / 81
    value = 1 / value
    valueDesc = "PythagoreanMinor6th_Inverted(81/128)"
    musicalRatios.append(Number(value, valueDesc))

    value = 32 / 27
    value = 1 / value
    valueDesc = "PythagoreanMinor3rd_Inverted(27/32)"
    musicalRatios.append(Number(value, valueDesc))

    value = 16 / 9
    value = 1 / value
    valueDesc = "PythagoreanMinor7th_Inverted(9/16)"
    musicalRatios.append(Number(value, valueDesc))

    value = 4 / 3
    value = 1 / value
    valueDesc = "PythagoreanPerfect4th_Inverted(3/4)"
    musicalRatios.append(Number(value, valueDesc))

    value = 1 / 1
    value = 1 / value
    valueDesc = "PythagoreanUnison_Inverted(1/1)"
    musicalRatios.append(Number(value, valueDesc))

    value = 3 / 2
    value = 1 / value
    valueDesc = "PythagoreanPerfect5th_Inverted(2/3)"
    musicalRatios.append(Number(value, valueDesc))

    value = 9 / 8
    value = 1 / value
    valueDesc = "PythagoreanMajor2nd_Inverted(8/9)"
    musicalRatios.append(Number(value, valueDesc))

    value = 27 / 16
    value = 1 / value
    valueDesc = "PythagoreanMajor6th_Inverted(16/27)"
    musicalRatios.append(Number(value, valueDesc))

    value = 81 / 64
    value = 1 / value
    valueDesc = "PythagoreanMajor3rd_Inverted(64/81)"
    musicalRatios.append(Number(value, valueDesc))

    value = 243 / 128
    value = 1 / value
    valueDesc = "PythagoreanMajor7th_Inverted(128/243)"
    musicalRatios.append(Number(value, valueDesc))

    value = 729 / 512
    value = 1 / value
    valueDesc = "PythagoreanAugmented4th_Inverted(512/729)"
    musicalRatios.append(Number(value, valueDesc))

def findPythagoreanIntervals():
    global musicalRatios

    value = 1024 / 729
    valueDesc = "PythagoreanDiminished5th(1024/729)"
    musicalRatios.append(Number(value, valueDesc))

    value = 256 / 243
    valueDesc = "PythagoreanMinor2nd(256/243)"
    musicalRatios.append(Number(value, valueDesc))

    value = 128 / 81
    valueDesc = "PythagoreanMinor6th(128/81)"
    musicalRatios.append(Number(value, valueDesc))

    value = 32 / 27
    valueDesc = "PythagoreanMinor3rd(32/27)"
    musicalRatios.append(Number(value, valueDesc))

    value = 16 / 9
    valueDesc = "PythagoreanMinor7th(16/9)"
    musicalRatios.append(Number(value, valueDesc))

    value = 4 / 3
    valueDesc = "PythagoreanPerfect4th(4/3)"
    musicalRatios.append(Number(value, valueDesc))

    value = 1 / 1
    valueDesc = "PythagoreanUnison(1/1)"
    musicalRatios.append(Number(value, valueDesc))

    value = 3 / 2
    valueDesc = "PythagoreanPerfect5th(3/2)"
    musicalRatios.append(Number(value, valueDesc))

    value = 9 / 8
    valueDesc = "PythagoreanMajor2nd(9/8)"
    musicalRatios.append(Number(value, valueDesc))

    value = 27 / 16
    valueDesc = "PythagoreanMajor6th(27/16)"
    musicalRatios.append(Number(value, valueDesc))

    value = 81 / 64
    valueDesc = "PythagoreanMajor3rd(81/64)"
    musicalRatios.append(Number(value, valueDesc))

    value = 243 / 128
    valueDesc = "PythagoreanMajor7th(243/128)"
    musicalRatios.append(Number(value, valueDesc))

    value = 729 / 512
    valueDesc = "PythagoreanAugmented4th(729/512)"
    musicalRatios.append(Number(value, valueDesc))


##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--JustIntonationIntervals",
                  action="store_true",
                  dest="JustIntonationIntervals",
                  default=False,
                  help="Print ratios for Just Intonation Intervals.")

parser.add_option("--JustIntonationIntervalsInverted",
                  action="store_true",
                  dest="JustIntonationIntervalsInverted",
                  default=False,
                  help="Print ratios for Just Intonation Intervals, inverted.")

parser.add_option("--PythagoreanIntervals",
                  action="store_true",
                  dest="PythagoreanIntervals",
                  default=False,
                  help="Print ratios for Pythagorean Intervals.")

parser.add_option("--PythagoreanIntervalsInverted",
                  action="store_true",
                  dest="PythagoreanIntervalsInverted",
                  default=False,
                  help="Print ratios for Pythagorean Intervals, inverted.")


# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print("RatioScript.py (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    sys.exit(0)

if (options.JustIntonationIntervals == True):
    # Clear out values in musicalRatios list.
    musicalRatios = list()

    # Get the ratios and put them in musicalRatios list.
    findJustIntonationIntervals()

    # Sort the values.
    sortedNumbers = sorted(musicalRatios, key=lambda c: c.value)

    # Print values.
    print("------------------------------------------------------------")
    for num in sortedNumbers:
        print("{:0.9f} {}".format(num.value, num.description))


if (options.JustIntonationIntervalsInverted == True):
    # Clear out values in musicalRatios list.
    musicalRatios = list()

    # Get the ratios and put them in musicalRatios list.
    findJustIntonationIntervalsInverted()

    # Sort the values.
    sortedNumbers = sorted(musicalRatios, key=lambda c: c.value)

    # Print values.
    print("------------------------------------------------------------")
    for num in sortedNumbers:
        print("{:0.9f} {}".format(num.value, num.description))

if (options.PythagoreanIntervals == True):
    # Clear out values in musicalRatios list.
    musicalRatios = list()

    # Get the ratios and put them in musicalRatios list.
    findPythagoreanIntervals()

    # Sort the values.
    sortedNumbers = sorted(musicalRatios, key=lambda c: c.value)

    # Print values.
    print("------------------------------------------------------------")
    for num in sortedNumbers:
        print("{:0.9f} {}".format(num.value, num.description))


if (options.PythagoreanIntervalsInverted == True):
    # Clear out values in musicalRatios list.
    musicalRatios = list()

    # Get the ratios and put them in musicalRatios list.
    findPythagoreanIntervalsInverted()

    # Sort the values.
    sortedNumbers = sorted(musicalRatios, key=lambda c: c.value)

    # Print values.
    print("------------------------------------------------------------")
    for num in sortedNumbers:
        print("{:0.9f} {}".format(num.value, num.description))

