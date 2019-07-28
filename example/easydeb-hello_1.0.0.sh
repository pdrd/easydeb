#!/bin/bash

RECIPE="./easydeb-hello_1.0.0.json"
BUILD="./"
OUT="./"

../src/easydeb "$RECIPE" "$BUILD" "$OUT"
