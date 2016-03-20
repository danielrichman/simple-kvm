#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

dpkg-deb --build manual-partitioning
mv manual-partitioning.deb extra/manual-partitioning.udeb
cp /usr/lib/debian-installer/images/8/amd64/text/debian-installer/amd64/initrd.gz .
gunzip initrd.gz 
(cd extra;  find . | fakeroot cpio --quiet -F ../initrd --append -o -H newc)
(cd extra2; find . | fakeroot cpio --quiet -F ../initrd --append -o -H newc)
gzip initrd 
