Name:		pandas
Version:	0.13.0
Release:	1%{?dist}
Summary:	Data analysis / manipulation library for Python

Group:		Development/Languages
License:	BSD 3-clause
URL:		https://github.com/pydata/pandas/archive/v%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python-setuptools,python-dateutil,Cython
BuildRequires:	python-devel
BuildRequires:	numpy >= 1.6.1
Requires:	numpy,python-dateutil,pytz

%description
pandas is a Python package providing fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data
both easy and intuitive. It aims to be the fundamental high-level building
block for doing practical, real world data analysis in Python. Additionally,
it has the broader goal of becoming the most powerful and flexible open
source data analysis / manipulation tool available in any language.


%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md RELEASE.md LICENSES LICENSE CONTRIBUTING.md
%{python_sitearch}/*


%changelog
* Tue Jan 14 2014 - 20140114-1 - Romain Acciari
- Initial release
