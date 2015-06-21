Name:		graph-explorer
Version:	1.2.0
Release:	3%{?dist}
Summary:	Graphite dashboard powered by structured metrics

Group:		Applications/Internet
License:	Apache License v2.0
URL:		https://github.com/vimeo/graph-explorer/archive/v1.2.0.tar.gz
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-httpd.conf
Source2:	%{name}.wsgi
Patch0:		%{name}-fix_path01.patch
Patch1:		%{name}-fix_collectd01.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

#BuildRequires:	
Requires:	python >= 2.6
Requires:	python-sqlite2,python-elasticsearch

%description
A highly interactive dashboard to satisfy varying ad-hoc information needs
across a multitude of metrics in a very powerful way:
- Core of graph-explorer is a database containing your metrics extended with tags
- You can use expressive queries which leverage this metadata to filter targets,
group them into graphs, process and aggregate them on the fly. Something like
SQL but metrics for rows and a list of graph definitions as a result set.
All graphs are built dynamically.


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build


%install
rm -rf %{buildroot}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datarootdir}/%{name} \
             $RPM_BUILD_ROOT/%{_datadir} \
             $RPM_BUILD_ROOT/%{_sharedstatedir}/%{name} \
             $RPM_BUILD_ROOT/%{_sysconfdir}/%{name} \
             $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d

# Copy everything
%{__cp} -a * $RPM_BUILD_ROOT/%{_datarootdir}/%{name}/

# Install configuration files to /etc and remove them from default directory
%{__install} config.py preferences.py $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/
%{__rm} -f $RPM_BUILD_ROOT/%{_datarootdir}/%{name}/{config.py*,preferences.py*}

# Install files for httpd WSGI support
%{__install} -m 644 %SOURCE1 $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__install} -m 755 %SOURCE2 $RPM_BUILD_ROOT/%{_datarootdir}/%{name}/%{name}.wsgi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.md TODO
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_datarootdir}/%{name}
%{_sharedstatedir}/%{name}
%ghost %attr(0644,root,root) %{_localstatedir}/log/%{name}.log
%ghost %attr(0644,root,root) %{_localstatedir}/log/httpd/%{name}-access.log
%ghost %attr(0644,root,root) %{_localstatedir}/log/httpd/%{name}-errors.log
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf


%changelog
* Wed Feb 26 2014 Romain Acciari <romain.acciari@worldline.com> 1.2.0-3
- Almost ready version
- httpd WSGI ready
* Tue Feb 25 2014 Romain Acciari <romain.acciari@worldline.com> 1.2.0-2
- Fix the source tarball
* Mon Feb 24 2014 Romain Acciari <romain.acciari@worldline.com> 1.2.0-1
- Initial release. For testing purpose only !
