#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

mkdir -p extra/etc/ssh
for type in rsa dsa ecdsa; do
    ssh-keygen -q -t $type -f extra/etc/ssh/ssh_host_${type}_key -N ''
    ssh-keygen -l -f extra/etc/ssh/ssh_host_${type}_key
done

cp /usr/lib/debian-installer/images/8/amd64/text/debian-installer/amd64/{linux,initrd.gz} .
gunzip initrd.gz 
(cd extra; find . | fakeroot cpio --quiet -F ../initrd --append -o -H newc)
gzip initrd 
