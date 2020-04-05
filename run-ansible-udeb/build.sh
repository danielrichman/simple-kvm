#!/bin/bash
set -o errexit -o nounset -o pipefail -o xtrace

test -d DEBIAN
mkdir -p .build .build/ansible-infra/callback-plugins
rsync -av DEBIAN/ .build/DEBIAN
cp debconf.py .build/ansible-infra/callback-plugins/
dpkg-deb --build .build ../preseed-utils/run-ansible.udeb
