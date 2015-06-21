Name:		redis-snmp
Version:	20120315
Release:	1%{?dist}
Summary:	Net-SNMP agent for Redis

Group:		HoneyComb
License:	GPL
URL:		https://github.com/masterzen/redis-snmp
Source0:	%{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
Requires:	redis,net-snmp,perl-Net-SNMP

%description
redis-snmp is a Redis Net-SNMP agent written in Perl, and using the Net-Snmp 
Perl bindings.

It connects to a redis server and returns information to Net-SNMP when needed.
It parses the Redis INFO command results.


%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p}	$RPM_BUILD_ROOT%{_sbindir} \
		$RPM_BUILD_ROOT%{_datadir}/snmp/mibs \
		$RPM_BUILD_ROOT%{_mandir}/man1
%{__install} -m 755 redis-snmp $RPM_BUILD_ROOT%{_sbindir}/
%{__install} -m 644 REDIS-SERVER-MIB.txt $RPM_BUILD_ROOT%{_datadir}/snmp/mibs/
%{__install} -m 644 redis-snmp.1 $RPM_BUILD_ROOT%{_mandir}/man1/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
/usr/sbin/redis-snmp
/usr/share/snmp/mibs/*
/usr/share/man/man1/*


%changelog
* Thu Mar 15 2012 Romain Acciari <romain.acciari@tos.net> - 20120315-1
- Initial release
