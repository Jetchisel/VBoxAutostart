VBoxAutostart
=============
Autostart and auto save of your vms during start up and shutdown of your host machine without doing your
favorite sudo or even su just to have your vms autostart and auto save. Enable the service one time and 
the vms you can set to auto via VBoxManage.

 This works with  systemd only.

1. Download the script that will handle the vms.

     wget https://raw.github.com/Jetchisel/systemd-vboxinit/master/systemd-vboxinit 

Copy it to your ~/bin directory.

      cp -v systemd-vboxinit ~/bin   

Make it executable.

     chmod ug+x ~/bin/systemd-vboxinit 


Change the group to vboxusers

     chgrp vboxusers ~/bin/systemd-vboxinit 


2. Download the unit file that will execute your script during boot/restart/shutdown of the host. Replace my username with the user who will run the vms.

     wget https://raw.github.com/Jetchisel/systemd-vboxinit/master/VBoXvmservice.service 

Replace my username in that file and copy that file to its destination as root.

     cp -v VBoXvmservice.service /usr/lib/systemd/ 

 Start that service.

     systemctl start VBoXvmservice.service 

Enable it .

     systemctl enable VBoXvmservice.service 

Check the status.

     systemctl status VBoXvmservice.service 



 3. Choose your vms that you want to autostart and autosave during boot/restart/shutdown of your host.

Get the names of the vms.

      VBoxManage list vms  

Set it to auto so the script will handle the autostart and autosave of the vm.

     VBoxManage setextradata YOUR-VM-NAME pvbx/startupMode auto 

Get the status.

      VBoxManage getextradata YOUR-VM-NAME pvbx/startupMode  

 Set it to manual if you dont want your vms to be handled by the script.

     VBoxManage setextradata YOUR-VM-NAME pvbx/startupMode manual 

 Using SetAuto script is another option to set your vms to auto or manual. 

 4. To access your vms.

     rdesktop localhost:1234 


where 1234 is the port number which you can set via the gui or via VBoxManage.  



NOTE: if you have the phpvirtualbox solution then you do not need this thus it can conflict with each other.
