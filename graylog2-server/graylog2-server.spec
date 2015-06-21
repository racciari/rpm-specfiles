Name:		graylog2-server
Version:	0.9.6
Release:	1%{?dist}
Summary:	Graylog2 is free and open source log management system

Group:		Log Management
License:	GPLv3
URL:		http://graylog2.org/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
Requires:	java-1.6.0-openjdk

%description
Graylog2 enables you to unleash the power that lays inside your logs.
Use it to run analytics, alerting, monitoring and powerful searches
over your whole log base. Need to debug a failing request? Just run
a quick filter search to find it and see what errors it produced.
Want to see all messages a certain API consumer is consuming in real
time? Create streams for every consumer and have them always only one
click away.


%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p}	$RPM_BUILD_ROOT%{_sysconfdir} \
		$RPM_BUILD_ROOT%{_bindir} \
		$RPM_BUILD_ROOT%{_datadir}/java
%{__install} graylog2.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/graylog2.conf
%{__install} bin/graylog2ctl $RPM_BUILD_ROOT%{_bindir}/
%{__install} graylog2-server.jar $RPM_BUILD_ROOT%{_datadir}/java/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*
%{_datadir}/java/*


%changelog
* Wed Feb 15 2012 Romain Acciari <romain.acciari@openio.io> - 0.9.6-1
- Initial release
