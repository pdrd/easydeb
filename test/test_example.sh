#!/bin/bash

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
EXAMPLE="$DIR/../example"
DEB="$EXAMPLE/easydeb-hello_1.0.0_amd64.deb"

[ -f "$DEB" ] && rm "$DEB"

"$EXAMPLE/build_deb.sh" > /dev/null 2>&1

[ ! -f "$DEB" ] && exit 1

SUCC=0
INFO="$(dpkg -I $EXAMPLE/easydeb-hello_1.0.0_amd64.deb)"

echo $INFO | grep -q "Package: easydeb-hello" && SUCC=$((SUCC+1))
echo $INFO | grep -q "Version: 1.0.0" && SUCC=$((SUCC+1))
echo $INFO | grep -q "Depends: " && SUCC=$((SUCC+1))
echo $INFO | grep -q "Section: misc" && SUCC=$((SUCC+1))
echo $INFO | grep -q "Priority: optional" && SUCC=$((SUCC+1))
echo $INFO | grep -q "Architecture: amd64" && SUCC=$((SUCC+1))
echo $INFO | grep -q "Installed-Size: 110" && SUCC=$((SUCC+1))
echo $INFO | grep -q "Maintainer: John Doe <john@example.com>" && SUCC=$((SUCC+1))
echo $INFO | grep -q "Description: Hello world example from easydeb." && SUCC=$((SUCC+1))

if [ "$SUCC" -lt 9 ]; then
    exit 1
fi

echo "test/test_example.sh successful"