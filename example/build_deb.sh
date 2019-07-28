#!/bin/bash

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
exec "$DIR/../bin/easydeb" "$DIR/hello.json"
