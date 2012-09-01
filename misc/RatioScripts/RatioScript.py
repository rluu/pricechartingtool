#!/usr/bin/env python3
##############################################################################
# File: RatioScript.py
#
# Author:  Ryan Luu     ryanluu@gmail.com
#
# Description:
#    Calculates a bunch of square roots, harmonic intervals,
#    and power calculations.  Then compares it with the given value
#    to find the closest values to it.
#
# Usage:
#   ./RatioScript.py --help
#   ./RatioScript.py --value=0.111
#
##############################################################################



##############################################################################

# For calling sys.exit(1), etc.
import sys 

# For parsing command-line options
from optparse import OptionParser  

# For square root and pi, etc.
import math

# Version string.
VERSION = "0.1"

global options
global roots
global powers
global fractionalRatios
global musicalRatios
global numbers

roots = list()
powers = list()
fractionalRatios = list()
musicalRatios = list()
numbers = list()

# This is the number to compare to all the square roots.  This value
# is set via the --value option.
numToCompare = 0.0


##############################################################################

class Number:
    def __init__(self, value=0.0, description=""):
        self.description = description
        self.value = value

    def toString(self):
        return "{},{}".format(self.description, self.value)
    
class Root(Number):
    pass

class Power(Number):
    pass

##############################################################################

def getRoots(root, begin, end):
    global roots
    
    for i in range(begin, end):
        value = math.pow(float(i), (1.0 / root))
        valueDesc = "{}-root({})".format(root, float(i))

        reciprocal = 1 / value
        reciprocalDesc = "1 / {}-root({})".format(root, float(i))

        roots.append(Root(value, valueDesc))
        roots.append(Root(reciprocal, reciprocalDesc))

def getPowers(power, begin, end):
    global powers
    
    for i in range(begin, end):
        value = math.pow(float(i), power)
        valueDesc = "pow({}, {})".format(float(i), power)

        reciprocal = 1 / value
        reciprocalDesc = "1 / pow({}, {})".format(float(i), power)

        powers.append(Power(value, valueDesc))
        powers.append(Power(reciprocal, reciprocalDesc))

def getSpecialPowers(begin, end):
    global powers
    phi = 1.61803399

    for power in range(begin, end):
        # Do Fibs.
        value = math.pow(phi, power)
        valueDesc = "pow(phi, {})".format(power)
        powers.append(Power(value, valueDesc))

        reciprocal = 1 / value
        reciprocalDesc = "1 / pow(phi, {})".format(power)
        powers.append(Power(reciprocal, reciprocalDesc))

def getFractionalRatios():
    global fractionalRatios

    # Septimal ratios.
    begin = 1
    end = 7
    denominator = 7
    
    for i in range(begin, end):
        value = i / denominator
        valueDesc = "{} / {}".format(i, denominator)
        
        fractionalRatios.append(Number(value, valueDesc))

def getMusicalRatios():
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

    ####################################################################

    # The above Pythagorean notes, but inverted ratios.
    
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

    ####################################################################

    # Just intonation.
    
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


    # The above, but with inverted ratios.
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



def findClosestNumbers(x, numNumbersToReturn=8):
    """x is a float"""
    
    global numbers

    closest = []
    diffs = []
    for number in numbers:
        if len(closest) < numNumbersToReturn:
            closest.append(number)
            diffs.append(abs(x - number.value))
        else:
            diff = abs(x - number.value)
            
            i = 0
            indexOfLargestDiff = -1
            largestDiff = 0
            for d in diffs:
                if d > largestDiff:
                    largestDiff = d
                    indexOfLargestDiff = i
                i += 1

            if diff < largestDiff:
                closest[indexOfLargestDiff] = number
                diffs[indexOfLargestDiff] = diff

    return sorted(closest, key=lambda c: c.value)

##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--value",
                  action="store",
                  type="float",
                  dest="value",
                  default=None,
                  help="Specify value to compare to all computed ratios.",
                  metavar="<VALUE>")

parser.add_option("--num-results",
                  action="store",
                  type="int",
                  dest="num_results",
                  default=8,
                  help="Specify number of results to return.",
                  metavar="<NUM_RESULTS>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print("RatioScript.py (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    sys.exit(0)

if (options.value == None):
    print("Error: Please specify a number to the --value option.")
    sys.exit(1)
else:
    numToCompare = options.value
    
numNumbersToReturn = options.num_results


# Do various calculations of ratios and numbers that I should pay
# attention to in the markets..
for i in range(1, 7):
    getRoots(i, 1, 288)
for i in range(1, 7):
    getPowers(i, 1, 64)
getSpecialPowers(1, 64)
getFractionalRatios()
getMusicalRatios()

# Append results to 'numbers' list.
for root in roots:
    numbers.append(root)
for power in powers:
    numbers.append(power)
for ratio in fractionalRatios:
    numbers.append(ratio)
for ratio in musicalRatios:
    numbers.append(ratio)

# Find the 'numNumbersToReturn' closest numbers to value 'numToCompare'.
closestNumbers = findClosestNumbers(numToCompare, numNumbersToReturn)

# Print results.
print("Closest numbers to {} are: ".format(numToCompare))
for num in closestNumbers:
    print(num.toString())

##############################################################################
