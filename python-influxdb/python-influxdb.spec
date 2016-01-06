%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%endif
%global pypi_name influxdb

Name:           python-influxdb
Version:        2.10.0
Release:        1%{?dist}
Summary:        Python client for interacting with InfluxDB
License:        MIT
URL:            https://github.com/influxdb/influxdb-python/
Source0:        https://pypi.python.org/packages/source/i/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-sphinx_rtd_theme
BuildRequires:  python-sphinx

Requires:       python-dateutil >= 2.0.0
Requires:       pytz
Requires:       python-six >= 1.9.0
Requires:       python-requests >= 2.5.2


%description
A python client to interact with InfluxDB

%if 0%{?with_python3}
%package -n python3-influxdb
Summary:        Python client for interacting with InfluxDB
BuildRequires:  python3-devel, python3-setuptools
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  python3-sphinx
Requires:       python3-pytz
Requires:       python3-dateutil >= 2.0.0
Requires:       python3-six >= 1.9.0
Requires:       python3-requests >= 2.5.2


%description -n python3-influxdb
A python client to interact with InfluxDB

%endif # with_python3


%prep
%setup -qc -n %{pypi_name}-%{version}
mv %{pypi_name}-%{version} python2
pushd python2
# Common docs
cp -a README.rst ../
popd

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find python2 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'


%build
pushd python2
%{__python2} setup.py build
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with_python3


%install
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
popd


%files
%{python2_sitelib}/influxdb
%{python2_sitelib}/influxdb*.egg-info
%doc README.rst 

%if 0%{?with_python3}
%files -n python3-influxdb
%{python3_sitelib}/influxdb
%{python3_sitelib}/influxdb*.egg-info
%doc README.rst
%endif # with_python3


%changelog
* Mon Jan 04 2016 Romain Acciari <romain.acciari@openio.io> 2.10.0
- Update version
* Wed Oct 14 2015 Pradeep Kilambi <pkilambi@redhat.com> 2.9.1
- initial package release
