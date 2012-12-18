#!/bin/bash

latexRootFilename="declination"
if [ -f "${latexRootFilename}.tex" ]
then
    latex "${latexRootFilename}.tex" && dvipdf "${latexRootFilename}.dvi"
    #okular "${latexRootFilename}.pdf"
fi

latexRootFilename="geoLatitude"
if [ -f "${latexRootFilename}.tex" ]
then
    latex "${latexRootFilename}.tex" && dvipdf "${latexRootFilename}.dvi"
    #okular "${latexRootFilename}.pdf"
fi

latexRootFilename="helioLatitude"
if [ -f "${latexRootFilename}.tex" ]
then
    latex "${latexRootFilename}.tex" && dvipdf "${latexRootFilename}.dvi"
    #okular "${latexRootFilename}.pdf"
fi

