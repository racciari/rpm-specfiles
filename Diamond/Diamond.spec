Name:		Diamond
Version:	4.0
Release:	1%{?dist}
Summary:	Smart data producer for graphite graphing package

License:	MIT
URL:		https://github.com/python-diamond/Diamond
Source0:	https://github.com/python-diamond/Diamond/archive/v%{version}/%{name}-%{version}.tar.gz

#BuildRequires:	
Requires:	python >= 2.6

%description
Diamond is a python daemon that collects system metrics and publishes
them to Graphite (and others). It is capable of collecting cpu, memory,
network, i/o, load and disk metrics. Additionally, it features an API
for implementing custom collectors for gathering metrics from almost
any source.


%prep
%setup -q


%build


%install
%{__python} setup.py install -O1 \
  --root=$RPM_BUILD_ROOT \
  --record=INSTALLED_FILES


%files
%doc



%changelog
* Thu Feb 05 2015 - 0.4-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
