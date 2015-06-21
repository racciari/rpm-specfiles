Name:           statsd
Version:        0.7.0
Release:        2%{?dist}
Summary:        Simple daemon for easy stats aggregation
Group:          Applications/Internet
License:        Etsy Open Source License
URL:            https://github.com/etsy/statsd/archive/v%{version}.tar.gz
Vendor:         Etsy
Source0:        %{name}-%{version}.tar.gz
Source1:	statsd.init
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
Requires:       nodejs

%description
A network daemon that runs on the Node.js platform and listens for
statistics, like counters and timers, sent over UDP and sends
aggregates to one or more pluggable backend services (e.g., Graphite).

%prep
%setup -q

%build

%install
%{__mkdir_p} %{buildroot}/usr/share/statsd/backends %{buildroot}/usr/share/statsd/lib
%{__install} -Dp -m0644 stats.js %{buildroot}/usr/share/statsd
%{__install} -Dp -m0644 lib/*.js %{buildroot}/usr/share/statsd/lib
%{__install} -Dp -m0644 backends/{console.js,graphite.js} %{buildroot}/usr/share/statsd/backends/

%{__mkdir_p} %{buildroot}%{_initrddir}
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__install} -Dp -m0644 exampleConfig.js  %{buildroot}%{_sysconfdir}/%{name}/config.js

%{__mkdir_p} %{buildroot}%{_localstatedir}/lock/subsys
touch %{buildroot}%{_localstatedir}/lock/subsys/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_localstatedir}/lib/%{name} \
    -s /sbin/nologin -c "%{name} daemon" %{name}
exit 0

%preun
service %{name} stop
exit 0

%postun
if [ $1 = 0 ]; then
	chkconfig --del %{name}
	getent passwd %{name} >/dev/null && \
	userdel -r %{name} 2>/dev/null
fi
exit 0

%post
chkconfig --add %{name}
service %{name} start

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md exampleConfig.js
/usr/share/%{name}
%{_initrddir}/%{name}
%config %{_sysconfdir}/%{name}
%ghost %{_localstatedir}/lock/subsys/%{name}

%changelog
* Fri Jan 10 2014 Romain Acciari <romain.acciari@openio.io> 0.7.0-2
- Fix node path in init
- Add lib/*.js files
* Fri Jan 10 2014 Romain Acciari <romain.acciari@openio.io> 0.7.0-1
- Bump to 0.7.0
* Sun Jun 10 2012 Rene Cunningham <rene@compounddata.com> 0.3.0-1
- initial build
