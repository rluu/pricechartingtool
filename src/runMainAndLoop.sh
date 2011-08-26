#!/bin/bash

SRCDIR=/home/rluu/programming/pricechartingtool/src

while true; do 
rm $SRCDIR/*.pyc
sleep 1
/usr/bin/python3 $SRCDIR/main.py
done
