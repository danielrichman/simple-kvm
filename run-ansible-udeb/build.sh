#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

test -d DEBIAN
mkdir -p .build
rsync -av DEBIAN/ .build/DEBIAN
dpkg-deb --build .build ../preseed-lib/run-ansible.udeb
