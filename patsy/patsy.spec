%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%if %{?el5}0
%{!?python26_sitearch: %define python26_sitearch %(%{__python}2.6 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python26_sitelib: %define python26_sitearch %(%{__python}2.6 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

Name:		patsy
Version:	0.2.1
Release:	1%{?dist}
Summary:	Python package for describing statistical models and building design matrices

Group:		Applications/Internet
License:	BSD
URL:		https://pypi.python.org/pypi/patsy
Source0:	https://pypi.python.org/packages/source/p/patsy/patsy-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

BuildRequires:	python-setuptools
Requires:	python

%description
A Python package for describing statistical models and for building design
matrices. It is closely inspired by and compatible with the 'formula'
mini-language used in R and S.


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
%doc LICENSE.txt README
%{python_sitearch}/*


%changelog
* Wed Jan 15 2014 Romain Acciari <romain.acciari@tos.net> - 0.2.1-1
- Initial release
