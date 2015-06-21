%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%if %{?el5}0
%{!?python26_sitearch: %define python26_sitearch %(%{__python}2.6 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python26_sitelib: %define python26_sitearch %(%{__python}2.6 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

Name:		statsmodels
Version:	0.5.0
Release:	1%{?dist}
Summary:	Python module to explore data, estimate statistical models, and perform statistical tests

Group:		Applications/Internet
License:	MIT
URL:		https://github.com/statsmodels/statsmodels/archive/v%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python-setuptools
BuildRequires:	numpy,scipy,pandas,patsy,Cython
Requires:	python,numpy,scipy,pandas,patsy

%description
Statsmodels is a Python module that allows users to explore data, estimate
statistical models, and perform statistical tests. An extensive list of
descriptive statistics, statistical tests, plotting functions, and result
statistics are available for different types of data and each estimator.
Researchers across fields may find that statsmodels fully meets their
needs for statistical computing and data analysis in Python.


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
%doc CHANGES.md CONTRIBUTING.rst COPYRIGHTS.txt INSTALL.txt LICENSE.txt README.txt
%{python_sitearch}/*


%changelog
* Wed Jan 15 2014 Romain Acciari <romain.acciari@tos.net> - 0.5.0-1
- Initial release
