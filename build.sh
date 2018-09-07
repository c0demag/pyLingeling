#!/bin/bash

LINGELING_DIR=lingeling
PYTHON=`which python`
#PYTHON=`which python3.5`
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $LINGELING_DIR
export CFLAGS=" -fPIC"
./configure.sh -O
make

cd $DIR
# SWIG (swig is handled within setup.py)
# swig -I${LINGELING_DIR} -python -o lingeling_python_wrap.c lingeling_python.i
# Build
$PYTHON ./setup.py build

# PKG (This is done by travis-CI. It is left here for reference)
# $PYTHON ./setup.py egg_info --tag-date --tag-build=.dev bdist_wheel
