#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

mkdir -p extra/etc/ssh
for type in rsa dsa ecdsa; do
    ssh-keygen -q -t $type -f extra/etc/ssh/ssh_host_${type}_key -N ''
    ssh-keygen -l -f extra/etc/ssh/ssh_host_${type}_key
done

INSTALLER=/usr/lib/debian-installer/images/10/amd64/text/debian-installer/amd64

cp $INSTALLER/linux .
cat \
    $INSTALLER/initrd.gz \
    <(cd extra; find -L . | cpio --quiet -R root -L -o -H newc | gzip --fast) \
    > initrd.gz
