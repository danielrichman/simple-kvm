#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

(cd ../manual-partitioning-udeb; ./build.sh)

cp /usr/lib/debian-installer/images/9/amd64/text/debian-installer/amd64/initrd.gz .
gunzip initrd.gz 
(cd extra; find -L . | fakeroot cpio --quiet -LF ../initrd --append -o -H newc)
gzip --fast initrd
