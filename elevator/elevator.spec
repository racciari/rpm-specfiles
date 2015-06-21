Name:		elevator
Version:	0.1
Release:	1%{?dist}
Summary:	Simple alerter based on SkyLine Horizon

Group:		System Environment/Daemons
License:	WTFPL
#URL:		
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

#BuildRequires:	
Requires:	skyline

%description
Simple alerter based on SkyLine Horizon.


%prep
%setup -q


%build


%install
rm -rf %{buildroot}
%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name} \
             ${RPM_BUILD_ROOT}/%{_datarootdir}/%{name} \
             ${RPM_BUILD_ROOT}/%{_initrddir}
%{__install} -m755 elevator.py ${RPM_BUILD_ROOT}/%{_datarootdir}/%{name}/
%{__install} -m644 config.py ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/
%{__install} -m644 %{name}.init ${RPM_BUILD_ROOT}/%{_initrddir}/%{name}


%post
if [ $1 -eq 1 ] ; then
  /sbin/chkconfig --add %{name} || :
fi


%preun
if [ $1 -eq 0 ] ; then
  /sbin/service %{name} stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name} || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sysconfdir}/%{name}
%{_datarootdir}/%{name}


%changelog
* Tue Mar 25 2014 - 0.1-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
