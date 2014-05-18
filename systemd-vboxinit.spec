#
# spec file for package 
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           systemd-vboxinit
Version:        1.6
Release:        1.6
License:        GPL-3.0+ 
Summary:        Auto start sessions when booting and save sessions when host is stopped
Url:            https://github.com/Jetchisel/VBoxAutostart
Group:          System/Management
Source0:        %{name}-%{version}
Source1:        %{name}_ManPage
Source2:        VBoxAutostart@.service
Source3:        ExtraData
Source4:        README
Source5:        %{name}.changes
Source6:        LICENSE
Source7:        %{name}.bash-completion
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
%if 0%{?suse_version} 
Requires(pre):  %fillup_prereq
%endif
BuildRequires:  ed
BuildRequires:  systemd
Requires:       systemd

%description
Auto start sessions when booting and save sessions when host is stopped with systemd

%if 0%{?suse_version} > 1220
%define _unitdir /usr/lib/systemd/system
%else
%define _unitdir /lib/systemd
%endif

%prep

%build

%install

mkdir -p %{buildroot}%{_usr}/lib/%{name}.d
install -Dm 0655 %{S:0} %{buildroot}%{_usr}/lib/%{name}.d/%{name}
install -Dm 0644 %{S:1} %{buildroot}%{_mandir}/man1/%{name}.1
install -Dm 0644 %{S:2} %{buildroot}%{_unitdir}/VBoxAutostart@.service
# Change oneshot to forking.
%if 0%{?suse_version} > 1230
cd %{buildroot}%{_unitdir}/ && printf '%s\n' 'g/oneshot/s//forking/' w q | ed -s VBoxAutostart@.service 
%endif
mkdir -p %{buildroot}%{_usr}/share/doc/packages/%{name}/
install -Dm 0644 %{S:3} %{buildroot}%{_usr}/share/doc/packages/%{name}/ExtraData
install -Dm 0644 %{S:4} %{buildroot}%{_usr}/share/doc/packages/%{name}/README
install -Dm 0644 %{S:5} %{buildroot}%{_usr}/share/doc/packages/%{name}/%{name}.changes
install -Dm 0644 %{S:6} %{buildroot}%{_usr}/share/doc/packages/%{name}/LICENSE
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -Dm 0644 %{S:7} %{buildroot}%{_sysconfdir}/bash_completion.d/

%pre
%service_add_pre VBoxAutostart@.service

%post

%if 0%{?suse_version} 
%{fillup_only -n systemd-boxinit}
%endif
%service_add_post VBoxAutostart@.service

%preun
%service_del_preun VBoxAutostart@.service

%postun
%service_del_postun VBoxAutostart@.service
%insserv_cleanup

%clean
%{?buildroot:%__rm -rf "%{buildroot}"}

%files
%defattr(-,root,root)
%{_usr}/lib/%{name}.d
%{_usr}/lib/%{name}.d/%{name}
%{_unitdir}/VBoxAutostart@.service
%{_usr}/share/doc/packages/%{name}
%doc %{_mandir}/man1/%{name}.1*
%config %{_sysconfdir}/bash_completion.d/%{name}.bash-completion

%changelog
* Sat May 10 06:36:54 UTC 2014 '<jetchisel@opensuse.org>'
- version 1.6
- Removed comm and ps, added killproc(8).
- Added the find command to list files inside /usr/lib/virtualbox and use pgrep to check if it is a running process.
- openSuSE has a killproc tool which is used to kill the daemons. If it is not available fall back to pkill :-).
- Fixed/improved some code in ExtraData script.

* Mon May  5 20:12:18 UTC 2014 '<jetchisel@opensuse.org>'
- Updated to version 1.6
- Added external commands comm and ps for processmanagenemt :-)

* Fri Apr 25 17:47:27 UTC 2014 '<jetchisel@opensuse.org>'
- Only short and long options remain in the options.
- Tab completion only works for long-options. (it is better this way :-))
- Added about and disable options.
- Switch to forking instead of oneshot (in the unit file type entry) for systemd-208 which is openSuSE 13.1
- The --disable option is useful before updating to another version of VirtualBox, to avoid install errors. (if any)
- Restart of vboxweb-service.service is needed after the disable option specially  when using app. such as phpvirtualbox.
- --stop is -x and --start is -s for short and long options.
- Grep is back :-), for checking vbox kernel modules.

* Thu Mar  6 20:44:05 UTC 2014 '<jetchisel@opensuse.org>'
- Improved the short and long options.

* Sat Feb 22 21:35:08 UTC 2014  '<jetchisel@opensuse.org>'
- Updated man page for the short and long options.

* Fri Feb 21 23:01:04 UTC 2014  '<jetchisel@opensuse.org>'
- Added support for long and short options for the OPTIONS.
- Added short and long options for bash_completion.
- Added additional checking if options/arguments is more than one.

* Wed Feb 19 04:29:58 UTC 2014 '<jetchisel@opensuse.org>'
- Save the Value of uuid and VmName variable in a Function to avoid repeating it twice. 

* Wed Feb 12 20:59:29 UTC 2014  '<jetchisel@opensuse.org>'
- Added the help function. 
- A more verbose explanation about the usage.
- Replaced ${0} with ${BASH_SOURCE}.

* Wed Jan 22 23:39:18 UTC 2014  '<jetchisel@opensuse.org>'
- Fix 'error broken pipe' by using a variable for the vms uuids instead of listing them using echo/printf.
- Removed the '2>/dev/null' from 'error broken pipe' which just redirects stderr to nothing.
- Added extglob so uuids can be tested in one line using '[[' instead of grep.
- Since grep is external to the shell it is now removed.
- The error 1 is replaced by 127 upon exit of systemd-vboxinit if it did not find VirtualBox or virtualbox.
- This means that an executable is not found in your system. eg the exit status of 'cnf'.
- See 'http://en.wikipedia.org/wiki/Exit_status' if you dont like 'man bash' EXIT STATUS section :-).

* Tue Jan 14 01:09:38 UTC 2014  '<jetchisel@opensuse.org>'
- Fix 'error broken pipe'
- If more than 5 vms are running the error broken pipe appears when stopping the daemon. (systemd!)
- While stopping systemd-vboxinit manually that 'broken pipe' does not appear.
- Added FD 7,8 and 9 to read inside the while loop.

* Thu Jan  9 07:46:08 UTC 2014  '<jetchisel@opensuse.org>'
- version systemd-vboxinit-1.5

* Thu Jan  2 02:20:08 UTC 2014 '<jetchisel@opensuse.org>'
- version 1.5
- bash_completion for the options.

* Thu Dec 26 2013 jetchisel@opensuse.org
- version 1.5

* Fri Dec 20 2013 jetchisel@opensuse.org
- version 1.0-98.1

* Mon Dec 10 2013 jetchisel@opensuse.org
- version 1.0-93.1

* Tue Dec 3 2013 jetchisel@opensuse.org
- Version 1.0-89.1

* Mon Oct 27 2013 jetchisel@opensuse.org
- initial packaging

