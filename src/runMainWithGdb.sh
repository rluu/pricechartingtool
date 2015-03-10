#!/bin/bash

SRCDIR=$( cd "$( dirname "$0" )" && pwd )
PYTHON="/usr/bin/env python3"

gdb --args ${PYTHON} ${SRCDIR}/main.py
