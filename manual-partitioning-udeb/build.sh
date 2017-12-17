#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

test -d DEBIAN
mkdir .build
cp -a DEBIAN .build/DEBIAN
dpkg-deb --build .build ../preseed-lib/manual-partitioning.udeb
