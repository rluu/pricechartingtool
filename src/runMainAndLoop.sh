#!/bin/bash

SRCDIR=/home/rluu/programming/pricechartingtool/src

while true; do 
rm $SRCDIR/*.pyc
/usr/bin/python3 $SRCDIR/main.py
done
