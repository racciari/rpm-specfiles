%define upstream_name hiredis
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:		python-%{upstream_name}
Version:	0.1.2
Release:	1%{?dist}
Summary:	Python extension that wraps hiredis

Group:		Development/Languages
License:	BSD
URL:		http://pypi.python.org/pypi/hiredis
Source0:	http://pypi.python.org/packages/source/h/hiredis/%{upstream_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python-devel
Requires:	hiredis

%description
Python extension that wraps hiredis

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%{python_sitearch}/%{upstream_name}
%{python_sitearch}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Mon Mar 10 2014 Romain Acciari <romain.acciari@worldline.com> - 0.1.2-1
- Initial release
