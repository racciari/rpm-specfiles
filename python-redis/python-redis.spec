%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name redis-py

Name:           python-redis
Version:        2.9.1
Release:        1%{?dist}
Summary:        A Python client for redis

Group:          Development/Languages
License:        MIT
URL:            http://github.com/andymccurdy/redis-py
Source0:        %{upstream_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if %{?el6}0
BuildRequires:  python-devel
%else
BuildRequires:  python26-devel
%endif

%description
This is a Python interface to the Redis key-value store.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%{__python}2.6 setup.py build

%install
rm -rf %{buildroot}
%{__python}2.6 setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README.rst
%if %{?el6}0
%{python_sitelib}/redis
%{python_sitelib}/redis-%{version}-*.egg-info
%else
/usr/lib/python2.6/site-packages/redis
/usr/lib/python2.6/site-packages/redis-%{version}-*.egg-info
%endif

%changelog
* Thu Mar 20 2014 Romain Acciari <romain.acciari@openio.io> - 2.9.1-1
- Bump to version 2.9.1
* Wed Mar 07 2012 Remi Nivet <remi.nivet@openio.io> - 2.4.11-1
- New version 2.4.11
* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 2.0.0-1
- Initial build
