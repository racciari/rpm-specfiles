%define debug_package %{nil}
%define base_install_dir %{_javadir}{%name}
%define __jar_repack %{nil}

Name:           logstash
Version:        1.3.3
Release:        1%{?dist}
Summary:        A tool for managing events and logs

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://logstash.net
Source0:        https://download.elasticsearch.org/logstash/logstash/%{name}-%{version}-flatjar.jar
Source1:        logstash.wrapper
Source2:        logstash.logrotate
Source3:        logstash.init
Source4:        logstash.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

#Requires:       jre7
Requires:       jre >= 1.7
Requires:       jpackage-utils

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
A tool for managing events and logs.


%prep


%build


%install
rm -rf $RPM_BUILD_ROOT

%{__mkdir_p} -v %{buildroot}%{_sysconfdir}/%{name} \
              %{buildroot}%{_datadir}/%{name}/{inputs,filters,outputs} \
              %{buildroot}%{_javadir}

              
# Install the JAR
%{__install} -v -p -m 644 %{SOURCE0} %{buildroot}%{_javadir}/%{name}.jar

# This is needed because Logstash will complain if there are no *.rb
# files in its Plugin directory
/bin/touch %{buildroot}%{_datadir}/%{name}/inputs/dummy.rb

# Wrapper script
%{__mkdir_p} -v %{buildroot}%{_bindir}
%{__install} -v -m 755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}

%{__sed} -i \
   -e "s|@@@NAME@@@|%{name}|g" \
   -e "s|@@@JARPATH@@@|%{_javadir}|g" \
   %{buildroot}%{_bindir}/%{name}

# Logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Misc
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/%{name}

# sysconfig and init
%{__mkdir} -p %{buildroot}%{_initddir}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 755 %{SOURCE3} %{buildroot}%{_initddir}/%{name}
%{__install} -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Using _datadir for PLUGINDIR because logstash expects a structure like logstash/{inputs,filters,outputs}
%{__sed} -i \
   -e "s|@@@NAME@@@|%{name}|g" \
   -e "s|@@@DAEMON@@@|%{_bindir}|g" \
   -e "s|@@@CONFDIR@@@|%{_sysconfdir}/%{name}|g" \
   -e "s|@@@LOCKFILE@@@|%{_localstatedir}/lock/subsys/%{name}|g" \
   -e "s|@@@LOGDIR@@@|%{_localstatedir}/log/%{name}|g" \
   -e "s|@@@PIDDIR@@@|%{_localstatedir}/run/%{name}|g" \
   -e "s|@@@PLUGINDIR@@@|%{_datadir}|g" \
   %{buildroot}%{_initddir}/%{name}

%{__sed} -i \
   -e "s|@@@NAME@@@|%{name}|g" \
   -e "s|@@@CONFDIR@@@|%{_sysconfdir}/%{name}|g" \
   -e "s|@@@LOGDIR@@@|%{_localstatedir}/log/%{name}|g" \
   -e "s|@@@PLUGINDIR@@@|%{_datadir}|g" \
   %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%pre
# create logstash group
if ! getent group logstash >/dev/null; then
    groupadd -r logstash
fi

# create logstash user
if ! getent passwd logstash >/dev/null; then
    useradd -r -g logstash -d %{_javadir}/%{name} \
            -s /sbin/nologin -c "logstash" logstash
fi

%post
/sbin/chkconfig --add logstash

%preun
if [ $1 -eq 0 ]; then
    /sbin/service logstash stop >/dev/null 2>&1
    /sbin/chkconfig --del logstash
fi

%postun
if getent group logstash >/dev/null; then
    groupdel logstash
fi
if getent passwd logstash >/dev/null; then
    userdel logstash
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_javadir}/*
%{_initddir}/%{name}
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}-indexer.conf
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}-shipper.conf
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
#%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%config(noreplace) %{_sysconfdir}/sysconfig/*

%defattr(-,%{name},%{name},-)
%{_localstatedir}/log/%{name}
%ghost %attr(0644,root,root) %{_localstatedir}/log/%{name}/%{name}-indexer.log
%ghost %attr(0644,root,root) %{_localstatedir}/log/%{name}/%{name}-shipper.log
%{_localstatedir}/run/%{name}

%changelog
* Fri May 23 2014 romain.acciari@openio.io 1.3.3-1
- Update to 1.3.3
- Fix an issue in S3 output

* Thu Jan 09 2014 romain.acciari@openio.io 1.3.2-1
- Update to 1.3.2

* Wed Nov 13 2013 romain.acciari@openio.io 1.2.1-2
- Fix JRE requires
- Add %postun

* Tue Nov 12 2013 romain.acciari@openio.io 1.2.1-1
- Reworked

* Wed Jun 12 2013 lars.francke@gmail.com 1.1.13-1
- Update logstash version to 1.1.13

* Thu May 09 2013 dmaher@mozilla.com 1.1.12-1
- Update logstash version to 1.1.12

* Thu Apr 25 2013 dmaher@mozilla.com 1.1.10-1
- Use flatjar instead of monolithic
- Update logstash version to 1.1.10

* Tue Jan 22 2013 dmaher@mozilla.com 1.1.9-1
- Add chkconfig block to init
- Update logstash version to 1.1.9

* Tue Jan 11 2013 lars.francke@gmail.com 1.1.5-1
- Initial version

