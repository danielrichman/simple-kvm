#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

test -d DEBIAN
mkdir -p .build .build/usr/share/ansible/plugins/callback
rsync -av DEBIAN/ .build/DEBIAN
cp debconf.py .build/usr/share/ansible/plugins/callback/
dpkg-deb --build .build ../preseed-lib/run-ansible.udeb
