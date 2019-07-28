#!/bin/bash

RECIPE="./easydeb-hello_1.0.0.json" # path to easydeb recipe file
BUILD="./" # path to binary files
OUT="./" # the .deb file will be placed here

../src/easydeb "$RECIPE" "$BUILD" "$OUT"
