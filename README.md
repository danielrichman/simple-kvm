Simple KVM script
=================

A single file dumb script to run KVM guests. It doesn't require a daemon, is
quite aggressive about dropping privileges, and helps with my odd networking
requirements.

To create a new guest
---------------------

 - `vim /etc/guests.json`
 - add the VM, but set
    - kernel: `/usr/lib/debian-installer/images/8/amd64/text/debian-installer/amd64/linux`
    - initrd: `/usr/local/lib/simple-kvm/guest-di-preseed/initrd.gz`
    - append: `console=ttyS0,115200n8`
 - `adduser --system --group guest-daniel-yocto --shell /bin/false`
 - `lvcreate vg0 --name daniel-yocto --size 8G`
 - `cd /usr/local/lib/system-kvm/guest-di-preseed`
 - `vim extra/early-commands`
    - set IP4, IP6, HOSTNAME
    - HOST4 should be the IPV4 of the host, not the guest.
