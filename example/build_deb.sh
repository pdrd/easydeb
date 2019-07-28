#!/bin/bash

DIR="$( cd "$(dirname "$0")" ; pwd -P )"

RECIPE="$DIR/hello.json" # path to easydeb recipe file
BUILD="$DIR" # path to binary files
OUT="$DIR" # the .deb file will be placed here

exec "$DIR/../src/easydeb" "$RECIPE" "$BUILD" "$OUT"
