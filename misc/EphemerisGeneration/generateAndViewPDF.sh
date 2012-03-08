#!/bin/bash

latexRootFilename="declination"
if [ -f "${latexRootFilename}.tex" ]
then
    latex "${latexRootFilename}.tex" && dvipdf "${latexRootFilename}.dvi"
    #okular "${latexRootFilename}.pdf"
fi

latexRootFilename="latitude"
if [ -f "${latexRootFilename}.tex" ]
then
    latex "${latexRootFilename}.tex" && dvipdf "${latexRootFilename}.dvi"
    #okular "${latexRootFilename}.pdf"
fi

