#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

(cd ../manual-partitioning-udeb; ./build.sh)

cat \
    /usr/lib/debian-installer/images/9/amd64/text/debian-installer/amd64/initrd.gz \
    <(cd extra; find -L . | cpio --quiet -R root -L -o -H newc | gzip --fast) \
    > initrd.gz
