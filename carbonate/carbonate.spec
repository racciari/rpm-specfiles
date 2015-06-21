%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%if %{?el5}0
%{!?python26_sitearch: %define python26_sitearch %(%{__python}2.6 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python26_sitelib: %define python26_sitearch %(%{__python}2.6 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

Name:		carbonate
Version:	0.2.0
Release:	1%{?dist}
Summary:	Utilities for managing Graphite clusters

Group:		Applications/Internet
License:	MIT
URL:		https://github.com/jssjr/carbonate/archive/%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

BuildRequires:	python-setuptools
Requires:	python,python-carbon,python-whisper
Requires:	python-twisted
#Requires:	python-twisted >= 11.1.0

%description
Graphite clusters are pretty cool. Here are some primitive tools to
help you manage your graphite clusters.

All of the tools support two common arguments; the path to a config file,
and the name of the cluster. Using these tools alongside a config file
that describes your graphite clusters you can build up scripts to manage
your metrics. Some of the tools could easily be replaced with one-liners
in shell, but exist here for convenience and readability. The goal is to
provide fast, predictable utilities that can easily be composed into more
advanced tooling.


%prep
%setup -q


%build
CFLAGS="%{optflags}" %{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

# Awful fix
[ "%{_libdir}" == "/usr/lib64" ] && [ -d $RPM_BUILD_ROOT/usr/lib ] \
  && %{__mv} $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/usr/lib64


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/*
%{python_sitearch}/*


%changelog
* Sun Jun 21 2015 Romain Acciari <romain.acciari@openio.io> - 0.2.0-1
- Initial release
