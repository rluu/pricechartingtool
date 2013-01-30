##############################################################################
README.txt

Current directory:
/home/rluu/programming/pricechartingtool/misc/BibleDownloadAndFormatting


Description:

The scripts in this directory facilitate in downloading various books of the KJV Bible from the website http://www.blueletterbible.org/ , and doing various operations on those downloaded HTML files such that the resulting HTML files on your computer contain the Bible books except with the modification of the Strong's Concordance Number superscript links showing text of the gematria value of those words instead of the Strong's Concordance Number.  The links still work to bring you to the lexicon page for that original Strong's Concordance Number word.  If you're on the computer, you can always hover the mouse over the link to see the associated Strong's Concordance Number.


The reason why I have created these scripts and done this is so that I can easily see the gematria values for myself, without having to do manual lookups for each word as I'm reading.  That why I can quickly do the necessary adding and arithmetic as I see fit.

##############################################################################

Steps to download and produce everything:



1) Run the scripts to download some books of the Bible. 

    ./getEzekiel.sh
    ./getDaniel.sh

This should create directories "Ezekiel" and "Daniel", respectively, in the current working directory, with HTML files within those directories for each chapter of the book(s).




2) The next step is to generate a CSV file with the mappings of Strong's Concordance Numbers to gematria values.  This is a time-intensive step and only needs to be done once to obtain the file!  Once done, it does not need to be done again, and you can go to the next step.  You can tell if it has already been done if the output file already exists and appears to be populated.

Open the file script file 'getAllStrongsConcordanceGematriaValues.py' and make sure all the global variables are set as desired (i.e. outputFilename is correct).  Most likely the defaults will be correct.  If it looks good, run the script, which will take about 105 minutes to complete.

    python3 getAllStrongsConcordanceGematriaValues.py

This should generate output file: 
/home/rluu/programming/pricechartingtool/misc/BibleDownloadAndFormatting/BibleGematriaValues.csv




3) The next step is to put the gematria values in those HTML files.  Open the script file 'convertHtmlFilesToIncludeGematriaValues.py' and make sure the global variables are set as desired.  Things to check are:

  - 'inputGematriaValuesCSVFilename' pointing to the input CSV file.

  - 'directoriesWithHtmlFilesForModification' contains the directories
    of Bible books' HTML files that we want to do modifications of.


Now run the script:

    python3 convertHtmlFilesToIncludeGematriaValues.py

This should make all the necessary modifications to your HTML files.  When execution is complete, you can open and view the files in firefox.  


##############################################################################
