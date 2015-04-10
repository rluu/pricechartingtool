#!/bin/bash
##############################################################################
# Description:
#   Removes all artifacts that have their tag set to something non-empty.
#
# Usage:
#   removeAllNonEmptyTags.bash /home/rluu/temp/Wheat_Daily.pcd
##############################################################################


##############################################################################
# Variables
##############################################################################

# Directory where this script resides.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd -P "$( dirname "$SOURCE" )" && pwd )"

# Top-level directory of pricechartingtool.
ROOTDIR=${DIR}/../..

#echo "ROOTDIR is: ${ROOTDIR}"

# PriceChartDocument file to operate on.
#PCDFILE=$ROOTDIR/data/PriceChartDocumentFiles/Wheat_Weekly_PriceData_1969_to_2008_and_TFC_2008_to_Current_Merged.pcd
PCDFILE=$1

##############################################################################


# Just list the unique tags.
#./modifyPriceChartDocument.py --pcd-file=$PCDFILE --script-file=$ROOTDIR/misc/PriceChartDocumentScripts/customScripts/listUniqueTags.py 2>&1

# Remove all of the artifacts with the non-empty tags.
for t in `./modifyPriceChartDocument.py --pcd-file=$PCDFILE --script-file=$ROOTDIR/misc/PriceChartDocumentScripts/customScripts/listUniqueTags.py 2>&1 | grep "Tag=" | cut -d"'" -f 2`; do ./modifyPriceChartDocument.py --pcd-file=$PCDFILE --script-file=$ROOTDIR/misc/PriceChartDocumentScripts/customScripts/removeArtifactsWithTag.py --tag=$t; done


##############################################################################
