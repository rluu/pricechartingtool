#!/bin/bash

SRCDIR=$( cd "$( dirname "$0" )" && pwd )

gdb --args /usr/bin/python3 $SRCDIR/main.py
