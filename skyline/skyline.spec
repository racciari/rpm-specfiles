Name:		skyline
Version:	20140114
Release:	5%{?dist}
Summary:	Real-time anomaly detection system

Group:		System Environment/Daemons
License:	MIT
URL:		https://github.com/etsy/skyline
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-horizon.init
Source2:	%{name}-analyzer.init
Source3:	%{name}-webapp.init
Patch0:		%{name}-variousfix3.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
Requires:	numpy,scipy,pandas,patsy,statsmodels,python-msgpack
Requires:	python-daemon,python-simplejson
Requires:	python-flask >= 0.9
# Got several problems with python-hiredis and old versions of python-redis
Requires:	python-redis >= 2.9.1
Conflicts:	python-hiredis

%description
Skyline is a real-time* anomaly detection* system*, built to enable passive
monitoring of hundreds of thousands of metrics, without the need to configure
a model/thresholds for each one, as you might do with Nagios. It is designed
to be used wherever there are a large quantity of high-resolution timeseries
which need constant monitoring. Once a metrics stream is set up (from StatsD
or Graphite or other source), additional metrics are automatically added to
Skyline for analysis. Skyline's easily extendible algorithms automatically
detect what it means for each metric to be anomalous. After Skyline detects
an anomalous metric, it surfaces the entire timeseries to the webapp,
where the anomaly can be viewed and acted upon.


%prep
%setup -q
%patch0 -p1

# Remove useless files
/bin/find ${RPM_BUILD_DIR} -type f -name '.gitignore' -exec rm -f {} \;


%build


%install
rm -rf %{buildroot}

# Install core
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/%{name}
%{__cp} -av src/{analyzer,horizon,webapp} $RPM_BUILD_ROOT/%{_datarootdir}/%{name}/

# Install default config file
%{__install} -Dv src/settings.py.example $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/settings.py
%{__install} -Dv bin/redis.conf $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/redis.conf.example

# Install init files
%{__install} -Dv %{SOURCE1} $RPM_BUILD_ROOT/%{_initddir}/skyline-horizon
%{__install} -Dv %{SOURCE2} $RPM_BUILD_ROOT/%{_initddir}/skyline-analyzer
%{__install} -Dv %{SOURCE3} $RPM_BUILD_ROOT/%{_initddir}/skyline-webapp

%{__mkdir_p} -v $RPM_BUILD_ROOT/%{_localstatedir}/{log,run,lib}/%{name} \
            $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/dump


%post
if [ $1 -eq 1 ] ; then
  /sbin/chkconfig --add %{name}-horizon || :
  /sbin/chkconfig --add %{name}-analyzer || :
  /sbin/chkconfig --add %{name}-webapp || :
fi

%preun
if [ $1 -eq 0 ] ; then
  /sbin/service %{name}-horizon stop > /dev/null 2>&1 || :
  /sbin/service %{name}-analyzer stop > /dev/null 2>&1 || :
  /sbin/service %{name}-webapp stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-horizon || :
  /sbin/chkconfig --del %{name}-analyzer || :
  /sbin/chkconfig --del %{name}-webapp || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.md readme.md requirements.txt
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_initddir}/*
%{_datarootdir}/%{name}
%{_localstatedir}/*/%{name}


%changelog
* Thu Mar 20 2014 Romain Acciari <romain.acciari@openio.io> 20140114-5
- Add chkconfig in %post and %preun
- New patch with force enable mini namespace
* Tue Mar 18 2014 Romain Acciari <romain.acciari@openio.io> 20140114-4
- Fix python-flask dependency
- Add new init scripts
* Tue Feb 20 2014 Romain Acciari <romain.acciari@openio.io> 20140114-3
- Additionnal fix to run on different port and use a file outside webapp directory
* Tue Feb 18 2014 Romain Acciari <romain.acciari@openio.io> 20140114-2
- Add patch (Fix init files, GRAPHITE_PORT, redis.conf.example, default configuration)
* Thu Feb 13 2014 Romain Acciari <romain.acciari@openio.io> 20140114-1
- Initial release
