VBoxAutostart
=============
Autostart and auto save of your vms during start up and shutdown of your host machine without doing your
favorite sudo or even su just to have your vms autostart and auto save. Enable the service one time and
the vms you can set to auto via VBoxManage.

 This works with  systemd only.


 At  creation time of the vms the extradata with the key pvbx/startupMode has no value.(Which is ignored)
 One need's to add the "auto" flag to the virtual machine in order for it  auto boot and auto save during
 startup and shutdown or reboot of the host.  The  virtual  machine  are  then  run  in the background.
 (which is what a daemon is all about :-)). One can access the virtual machines by using ssh(1) or with
 the gui tools such as  Krdc for KDE and the equivalent for other DE's. Example of commands are:

LIST VMS.
```shell
VBoxManage list vms
```

SET THE "AUTO" FLAG TO THE VMS.
```shell
VBoxManage setextradata vm-name pvbx/startupMode auto
```

SET THE "MANUAL" FLAG TO THE VMS.
```shell
VBoxManage setextradata vm-name pvbx/startupMode manual
```
Where "vm-name" is the name of the virtual machine.


## NOTE
  It is not recommended to run the script with root's right such as running it with the all time
  favorite sudo utility.  Once one  have  set the  "auto"  flag  to  the  virtual  machines one
  can test the script. Invoke it as a normal user that belongs to the vboxusers group.
  (It should be in once PATH so absolute path is not necessary.)
```shell
systemd-vboxinit --start

systemd-vboxinit --stop
```

One should see the virtual machines starting and saving state. If that succeeded one can enable
the daemon and reboot.


## USING THE DAEMON
* Start the service.

```shell
systemctl start VBoxAutostart@foo
```
* Enable the service.

```shell
systemctl enable VBoxAutostart@foo
```

* Check the status of the service

```shell
systemctl status VBoxAutostart@foo

journalctl _SYSTEMD_UNIT=VBoxAutostart@foo.service
```
* Restart the service.

```shell
systemctl restart VBoxAutostart@foo
```
Where foo is the username of the user who will use systemd-vboxinit.
