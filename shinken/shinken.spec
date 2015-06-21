%global with_systemd 0%{?fedora} >= 17
%global shinken_user shinken
%global shinken_group shinken

Summary:        Python Monitoring tool
Name:           shinken
Version:        1.2.4
Release:        3%{?dist}
URL:            http://www.%{name}-monitoring.org
Source0:        http://www.%{name}-monitoring.org/pub/%{name}-%{version}.tar.gz
Source1:        %{name}-commands.cfg
License:        AGPLv3+
Group:          Monitoring tools
#Patch0:         %{name}-webui-menu.patch
Requires:       python 
Requires:       python-pyro 
Requires:       python-simplejson 
%if %{with_systemd}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post):  chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
%endif
Requires:       nmap 
Requires:       sudo  
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if %{with_systemd}
BuildRequires:  systemd-units
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
Buildarch:      noarch

%description 
Shinken is a new monitoring tool written in Python. 
The main goal of Shinken is to allow users to have a fully flexible 
architecture for their monitoring system that can easily scale to large 
environments.
Shinken also provide interfaces with NDODB and Merlin database, 
Livestatus connector Shinken does not include any human interfaces.

%package arbiter
Summary: Shinken Arbiter 
Group:   Monitoring tools
Requires: %{name} = %{version}-%{release}

%description arbiter
Shinken arbiter daemon

%package reactionner
Summary: Shinken Reactionner
Group:   Monitoring tools
Requires: %{name} = %{version}-%{release}

%description reactionner
Shinken reactionner daemon

%package scheduler
Summary: Shinken Scheduler
Group:   Monitoring tools
Requires: %{name} = %{version}-%{release}

%description scheduler
Shinken scheduler daemon

%package poller
Summary: Shinken Poller
Group:   Monitoring tools
Requires: %{name} = %{version}-%{release}
Requires: nagios-plugins-all

%description poller
Shinken poller daemon

%package broker
Summary: Shinken Poller
Group:   Monitoring tools
Requires: %{name} = %{version}-%{release}
Requires: mysql-connector-python
Requires: python-redis
Requires: python-memcached
Requires: pymongo
Requires: mongodb-server

%description broker
Shinken broker daemon

%package receiver
Summary: Shinken Poller
Group:   Monitoring tools
Requires: %{name} = %{version}-%{release}

%description receiver
Shinken receiver daemon

%prep

%setup -q
#%patch0 -p1 -b .patch

# clean git files/
find . -name '.gitignore' -exec rm -f {} \;

# Check confuguration files 
sed -i -e 's!./$SCRIPT!python ./$SCRIPT!' test/quick_tests.sh
sed -i -e 's!include var/void_for_git!exclude var/void_for_git!'  MANIFEST.in

rm -rf  shinken/webui/plugins/eue shinken/webui/plugins/mobile/htdocs/css/log.css shinken/webui/plugins/mobile/htdocs/css/system.css shinken/webui/plugins/mobile/htdocs/css/details.css etc/packs/os/collectd/discovery.cfg etc/packs/databases/mongodb/macros.cfg shinken/webui/plugins_skonf bin/shinken-skonf

%build

%{__python} setup.py build 

%install

find %{buildroot} -size 0 -delete

%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-scripts=/usr/sbin/ --owner %{shinken_user} --group %{shinken_group}

install -d -m0755 %{buildroot}%{_sbindir}
install -p -m0755 bin/shinken-{arbiter,admin,discovery,broker,poller,reactionner,receiver,scheduler} %{buildroot}%{_sbindir}

install -d -m0755 %{buildroot}%{python_sitelib}/%{name}
install -p %{name}/*.py %{buildroot}%{python_sitelib}/%{name}
cp -rf %{name}/{clients,core,misc,modules,objects,plugins,webui} %{buildroot}%{python_sitelib}/%{name}

install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/
rm -rf %{buildroot}%{_sysconfdir}/%{name}/*

install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/objects
install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/objects/{contacts,discovery,hosts,services}

install -p -m0644 for_fedora/etc/objects/contacts/nagiosadmin.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/contacts/nagiosadmin.cfg
install -p -m0644 for_fedora/etc/objects/hosts/localhost.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/hosts/localhost.cfg
install -p -m0644 for_fedora/etc/objects/services/linux_disks.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/services/linux_disks.cfg
install -p -m0644 for_fedora/etc/htpasswd.users %{buildroot}%{_sysconfdir}/%{name}/htpasswd.users
install -p -m0644 for_fedora/etc/%{name}-specific.cfg %{buildroot}%{_sysconfdir}/%{name}/
install -p -m0644 for_fedora/etc/discovery*.cfg %{buildroot}%{_sysconfdir}/%{name}/
install -p -m0644 for_fedora/etc/{contactgroups,nagios,timeperiods,%{name}-specific,escalations,servicegroups,resource,templates}.cfg %{buildroot}%{_sysconfdir}/%{name}/
install -p -m0644 for_fedora/etc/{brokerd,pollerd,reactionnerd,receiverd,schedulerd}.ini %{buildroot}%{_sysconfdir}/%{name}/

cp %{SOURCE1}  %{buildroot}%{_sysconfdir}/%{name}/commands.cfg

%if %{with_systemd}
  install -d -m0755 %{buildroot}%{_unitdir}
  install -p -m0644 for_fedora/systemd/%{name}-arbiter.service %{buildroot}%{_unitdir}/%{name}-arbiter.service
  install -p -m0644 for_fedora/systemd/%{name}-broker.service %{buildroot}%{_unitdir}/%{name}-broker.service
  install -p -m0644 for_fedora/systemd/%{name}-reactionner.service %{buildroot}%{_unitdir}/%{name}-reactionner.service
  install -p -m0644 for_fedora/systemd/%{name}-scheduler.service %{buildroot}%{_unitdir}/%{name}-scheduler.service
  install -p -m0644 for_fedora/systemd/%{name}-receiver.service %{buildroot}%{_unitdir}/%{name}-receiver.service
  install -p -m0644 for_fedora/systemd/%{name}-poller.service %{buildroot}%{_unitdir}/%{name}-poller.service
%else
  install -d -m0755 %{buildroot}%{_initrddir}
  install -p -m0644 for_fedora/init.d/%{name}-arbiter %{buildroot}%{_initrddir}/%{name}-arbiter
  install -p -m0644 for_fedora/init.d/%{name}-scheduler %{buildroot}%{_initrddir}/%{name}-scheduler
  install -p -m0644 for_fedora/init.d/%{name}-poller %{buildroot}%{_initrddir}/%{name}-poller
  install -p -m0644 for_fedora/init.d/%{name}-broker %{buildroot}%{_initrddir}/%{name}-broker
  install -p -m0644 for_fedora/init.d/%{name}-reactionner %{buildroot}%{_initrddir}/%{name}-reactionner
  install -p -m0644 for_fedora/init.d/%{name}-receiver %{buildroot}%{_initrddir}/%{name}-receiver
%endif

install -d -m0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m0644 for_fedora/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/shinken

install -d -m0755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m0644  for_fedora/%{name}-tmpfiles.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}/archives
install -d -m0755 %{buildroot}%{_localstatedir}/lib/%{name}

mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m0755 %{buildroot}%{_localstatedir}/run/%{name}

install -d -m0755 %{buildroot}%{_usr}/lib/%{name}/plugins
install  -m0755 libexec/*.py libexec/discovery/*.py %{buildroot}%{_usr}/lib/%{name}/plugins

install -d -m0755 %{buildroot}%{_mandir}/man3
install -p -m0644 doc/man/* %{buildroot}%{_mandir}/man3

for lib in %{buildroot}%{python_sitearch}/%{name}/*.py; do
 sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

for Files in %{buildroot}%{python_sitelib}/%{name}/__init__.py %{buildroot}%{python_sitelib}/%{name}/core/__init__.py %{buildroot}%{python_sitelib}/%{name}/daemons/*.py %{buildroot}%{python_sitelib}/%{name}/modules/{openldap_ui.py,nrpe_poller.py,livestatus_broker/livestatus_query_cache.py} ; do
  %{__sed} -i.orig -e 1d ${Files}
  touch -r ${Files}.orig ${Files}
  %{__rm} ${Files}.orig
done


chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/shinken-greeting.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/views/log.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/login/htdocs/css/login.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/jquery.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/application.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/eltdetail/htdocs/js/domtab.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/views/dashboard.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/problems/views/widget_problems.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/fullscreen.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/README.md
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/bootstrap.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/shinken-currently.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/impacts/views/impacts.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/js/jquery.jclock.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/widget.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/pagination_element.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/custom/layout.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/fullscreen-widget.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/bootstrap.min.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/font/fontawesome-webfont.svg
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/header_element.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/dashboard.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap-scrollspy.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins_hostd/login/htdocs/js/jQuery.dPassword.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/widget.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins_hostd/login/htdocs/css/login.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/jquery.meow.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/problems/views/widget_last_problems.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/eltdetail/htdocs/css/eltdetail.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/htdocs/css/system.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/views/fullscreen.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/elements/jquery.meow.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap-carousel.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/footer_element.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/htdocs/css/log.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/problems/views/problems.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap.min.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/google-code-prettify/prettify.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/impacts/htdocs/css/impacts.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/views/currently.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/login/views/login.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap-typeahead.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/views/system.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/google-code-prettify/prettify.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/eltdetail/views/eltdetail.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/docs.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/layout.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/font-awesome.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/font-awesome-ie7.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/shinkenui.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/views/system_widget.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap-alert.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/custom/badger.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/navigation_element.tpl


sed -i -e 's!/usr/local/shinken/libexec!%{_libdir}/nagios/plugins!' %{buildroot}%{_sysconfdir}/%{name}/resource.cfg
sed -i -e 's!/usr/lib/nagios/plugins!%{_libdir}/nagios/plugins!' %{buildroot}%{_sysconfdir}/%{name}/resource.cfg
sed -i -e 's!/usr/local/shinken/var/arbiterd.pid!/var/run/shinken/arbiterd.pid!' %{buildroot}%{_sysconfdir}/%{name}/nagios.cfg
sed -i -e 's!command_file=/usr/local/shinken/var/rw/nagios.cmd!command_file=/var/log/shinken/nagios.cmd!' %{buildroot}%{_sysconfdir}/%{name}/nagios.cfg
sed -i -e 's!cfg_file=hostgroups.cfg!!' %{buildroot}%{_sysconfdir}/%{name}/nagios.cfg
sed -i -e 's!,Windows_administrator!!' %{buildroot}%{_sysconfdir}/%{name}/contactgroups.cfg
sed -i -e 's!/usr/local/shinken/src/!/usr/sbin/!' FROM_NAGIOS_TO_SHINKEN
sed -i -e 's!/usr/local/nagios/etc/!/etc/shinken/!' FROM_NAGIOS_TO_SHINKEN
sed -i -e 's!/usr/local/shinken/src/etc/!/etc/shinken/!' FROM_NAGIOS_TO_SHINKEN
sed -i -e 's!(you can also be even more lazy and call the bin/launch_all.sh script).!!' FROM_NAGIOS_TO_SHINKEN

rm -rf %{buildroot}%{_localstatedir}/{log,run,lib}/%{name}/void_for_git
rm %{buildroot}%{_sysconfdir}/default/shinken
rm -rf %{buildroot}%{_sysconfdir}/init.d/shinken*
rm -rf %{buildroot}%{_usr}/lib/%{name}/plugins/*.{pyc,pyo}
rm -rf %{buildroot}%{_sbindir}/shinken-{arbiter,discovery,broker,poller,reactionner,receiver,scheduler}.py

find  %{buildroot}%{python_sitelib}/%{name} -type f | xargs sed -i 's|#!/usr/bin/python||g' 

chmod +x %{buildroot}%{python_sitelib}/%{name}/{acknowledge.py,trigger_functions.py,__init__.py,action.py,db_sqlite.py,dependencynode.py,satellite.py,bin.py,notification.py,sorteddict.py,skonfuiworker.py,arbiterlink.py,eventhandler.py,autoslots.py,modulesmanager.py,borg.py,memoized.py,singleton.py}

sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python_sitelib}/%{name}/webui/plugins/mobile/mobile.py
sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python_sitelib}/%{name}/modules/webui_broker/helper.py
sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python_sitelib}/%{name}/webui/plugins/mobile/mobile.py
sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python_sitelib}/%{name}/modules/webui_broker/helper.py
rm -rf  %{buildroot}%{python_sitelib}/%{name}/webui/plugins/user/{__init__.pyo,__init__.pyc}
rm -rf  %{buildroot}%{python_sitelib}/%{name}/webui/plugins/eue
chmod -x %{buildroot}%{python_sitelib}/%{name}/{acknowledge.py,trigger_functions.py,__init__.py}

%clean

%pre 
getent group %{shinken_group} >/dev/null || groupadd -r %{shinken_group}
getent passwd %{shinken_user} >/dev/null || useradd -r -g %{shinken_group} -d %{_localstatedir}/spool/nagios -s /sbin/nologin %{shinken_user}
exit 0

%post arbiter
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-arbiter || :
  %endif
fi

%post broker
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-broker || :
%endif
fi

%post poller
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-poller || :
  %endif
fi

%post reactionner
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-reactionner || :
%endif
fi

%post scheduler
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-scheduler || :
  %endif
fi

%post receiver
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-receiver || :
  %endif
fi

%preun arbiter 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-arbiter.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-arbiter.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-arbiter stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-arbiter || :
  %endif
fi

%preun broker 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-broker.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-broker.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-broker stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-broker || :
  %endif
fi

%preun poller 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-poller.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-poller.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-poller stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-poller || :
  %endif
fi

%preun reactionner 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-reactionner.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-reactionner.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-reactionner stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-reactionner || :
  %endif
fi

%preun scheduler 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-scheduler.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-scheduler.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-scheduler stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-scheduler || :
  %endif
fi

%preun receiver 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-receiver.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-receiver.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-receiver stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-receiver || :
  %endif
fi

%postun arbiter
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-arbiter.service >/dev/null 2>&1 || :
  fi
%endif

%postun broker
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-broker.service >/dev/null 2>&1 || :
  fi
%endif

%postun poller
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-poller.service >/dev/null 2>&1 || :
  fi
%endif

%postun reactionner
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-reactionner.service >/dev/null 2>&1 || :
  fi
%endif

%postun scheduler
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-scheduler.service >/dev/null 2>&1 || :
  fi
%endif

%postun receiver
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-receiver.service >/dev/null 2>&1 || :
  fi
%endif

%files arbiter
%if %{with_systemd}
  %{_unitdir}/%{name}-arbiter.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-arbiter
%endif
%{_sbindir}/%{name}-arbiter*
%{_mandir}/man3/%{name}-arbiter*

%files reactionner
%if %{with_systemd}
  %{_unitdir}/%{name}-reactionner.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-reactionner
%endif
%{_sbindir}/%{name}-reactionner*
%{_mandir}/man3/%{name}-reactionner*

%files scheduler
%if %{with_systemd}
  %{_unitdir}/%{name}-scheduler.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-scheduler
%endif
%{_sbindir}/%{name}-scheduler*
%{_mandir}/man3/%{name}-scheduler*

%files poller
%if %{with_systemd}
  %{_unitdir}/%{name}-poller.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-poller
%endif
%{_sbindir}/%{name}-poller*
%{_mandir}/man3/%{name}-poller*

%files broker
%if %{with_systemd}
  %{_unitdir}/%{name}-broker.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-broker
%endif
%{_sbindir}/%{name}-broker*
%{_mandir}/man3/%{name}-broker*

%files receiver
%if %{with_systemd}
  %{_unitdir}/%{name}-receiver.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-receiver
%endif
%{_sbindir}/%{name}-receiver*
%{_mandir}/man3/%{name}-receiver*

%files
%{python_sitelib}/%{name}
%if %{with_systemd}
%{python_sitelib}/Shinken-%{version}-py2.7.egg-info
%else
%{python_sitelib}/Shinken-%{version}-py2.6.egg-info
%endif
%{_sbindir}/%{name}-receiver*
%{_sbindir}/%{name}-discovery
%{_sbindir}/%{name}-admin
%{_sbindir}/%{name}-hostd
%{_sbindir}/%{name}-packs
%doc etc/packs COPYING THANKS 
%{_mandir}/man3/%{name}-*
%{_usr}/lib/%{name}/plugins
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/log/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/lib/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/run/%{name}

%changelog
* Mon Feb 25 2013 Romain Acciari <romain.acciari@openio.io> - 1.2.4-3
- Add discovery modules

* Fri Feb 22 2013 Romain Acciari <romain.acciari@openio.io> - 1.2.4-2
- Add mongodb dependency to broker (for WebUI)

* Thu Feb 21 2013 Romain Acciari <romain.acciari@openio.io> - 1.2.4-1
- update from upstream
- Build for CentOS6

* Sat Dec 15 2012 David Hannequin <david.hannequin@gmail.com> - 1.2.2-1
- update from upstream,
- delete eue module,
- Fix web site url, 
- Fix Bug 874092 (thanks Sébastien Andreatta).

* Fri Dec 14 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-7
- Fix uninstall receiver.  

* Wed Nov 5 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-6
- Fix bug 874089.  

* Sun Sep 16 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-5
- Add support of el6,
- Remove shebang from Python libraries,
- Delete echo printing,
- Remove CFLAGS.

* Mon Sep 10 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-4
- Add COPYING README THANKS file,
- delete defattr.

* Sun Sep 09 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-3
- Delete require python-sqlite2.

* Sun Jul 22 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-2
- Add build patch. 

* Tue Mar 13 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-1
- Update from upstream,
- Add shinken packs

* Mon Oct 24 2011 David Hannequin <david.hannequin@gmail.com> - 0.8.1-1
- Update from upstream,
- Add manpage, 
- Add require nagios plugins.  

* Mon May 30 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.5-1
- Update from upstream,
- Add require python-redis, 
- Add require python-memcached.

* Mon May 30 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-3
- Fix path in default shinken file,
- Fix path in setup.cfg, 
- Add file FROM_NAGIOS_TO_SHINKEN.

* Sun May 29 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-2
- Fix shinken configuration,
- Replace macro,
- Update from upstreamr.

* Fri May 20 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-1
- Update from upstream. 

* Sun Apr 29 2011 David Hannequin <david.hannequin@gmail.com> - 0.6-1
- Fisrt release for fedora.
