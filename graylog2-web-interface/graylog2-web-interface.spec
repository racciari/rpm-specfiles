Name:		graylog2-web-interface
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


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README


%changelog
* Wed Feb 15 2012 Romain Acciari <romain.acciari@openio.io> - 0.9.6-1
- Initial release
