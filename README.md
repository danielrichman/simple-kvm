Simple KVM script
=================

A single file dumb script to run KVM guests. It doesn't require a daemon, is
quite aggressive about dropping privileges, and helps with my odd networking
requirements.

To install
----------

As root,

 - `apt install qemu-kvm`
 - `git clone https://github.com/danielrichman/simple-kvm /usr/local/lib/simple-kvm`
 - `ln -s /usr/local/lib/simple-kvm/guest-manager /usr/local/bin`
 - `ln -s /usr/local/lib/simple-kvm/random-mac    /usr/local/bin`
 - `cp /usr/local/lib/simple-kvm/simple-kvm\@.service /etc/systemd/system/simple-kvm\@.service`

To create a new guest
---------------------

 - `vim /etc/guests.json`: add the VM, but set
    - kernel: `/usr/lib/debian-installer/images/11/amd64/text/debian-installer/amd64/linux`
    - initrd: `[ "/usr/lib/debian-installer/images/11/amd64/text/debian-installer/amd64/initrd.gz", "/usr/local/lib/simple-kvm/guest-di-preseed/extra/" ]`
    - append: `console=ttyS0,115200n8`
 - `adduser --system --group guest-daniel-yocto --shell /bin/false`
 - `lvcreate vg0 --name daniel-yocto --size 8G`
 - `cd /usr/local/lib/simple-kvm/guest-di-preseed`
 - `vim extra/preseed-settings`
    - set IP4, IP6, HOSTNAME
    - HOST4 should be the IPV4 of the host, not the guest.
 - edit the authorized keys in `extra/late-commands`
 - `(cd manual-partitioning-udeb; ./build.sh)`
 - `guest-manager daniel-yocto boot`
    - let it do its thing, takes about 5mins
    - you can use `guest-manager daniel-yocto console` to watch
 - `vim /etc/guests.json`: change the kernel, initrd to their final values
    - to direct boot the kernel from the host, use `/vmlinuz` `/initrd.img` `console=ttyS0,115200n8 root=/dev/vda`
    - to use grub omit the three options (and change the preseed to install grub)
 - `systemctl enable simple-kvm@daniel-yocto.service`
 - `systemctl start simpke-kvm@daniel-yocto.service`

Todo
----

 - RAID monitoring
 - Add a helper to guest-manager to do installs. Pass the v4 and v6 on the kernel command line so that the initrd can be reused.
