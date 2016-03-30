Simple KVM script
=================

A single file dumb script to run KVM guests. It doesn't require a daemon, is
quite aggressive about dropping privileges, and helps with my odd networking
requirements.

To create a new guest
---------------------

 - `vim /etc/guests.json`: add the VM, but set
    - kernel: `/usr/lib/debian-installer/images/8/amd64/text/debian-installer/amd64/linux`
    - initrd: `/usr/local/lib/simple-kvm/guest-di-preseed/initrd.gz`
    - append: `console=ttyS0,115200n8`
 - `adduser --system --group guest-daniel-yocto --shell /bin/false`
 - `lvcreate vg0 --name daniel-yocto --size 8G`
 - `cd /usr/local/lib/simple-kvm/guest-di-preseed`
 - `vim extra2/early-commands-settings`
    - set IP4, IP6, HOSTNAME
    - HOST4 should be the IPV4 of the host, not the guest.
 - edit `extra2/authorized_keys`
 - `./build.sh`
 - `guest-manager daniel-yocto boot`
    - let it do its thing, takes about 5mins
    - you can use `guest-manager daniel-yocto console` to watch
 - `vim /etc/guests.json`: change the kernel, initrd to their final values
    - to direct boot the kernel from the host, use `/vmlinuz` `/initrd.img` `console=ttyS0,115200n8 root=/dev/vda`
    - to use grub omit the three options (and change the preseed to install grub)
 - `cp /usr/local/lib/simple-kvm/guest-example.service /etc/systemd/system/guest-daniel-yocto.service`
 - `vim /etc/systemd/system/guest-daniel-yocto.service` and find-replace the name
 - `systemctl enable guest-daniel-yocto.service`
 - `systemctl start guest-daniel-yocto.service`

Todo
----

 - RAID monitoring
 - can we use systemd templated services instead of multiple services?
 - Add a helper to guest-manager to do installs. Pass the v4 and v6 on the kernel command line so that the initrd can be reused.
