%global tarball_name elasticsearch-py

Name:		python-elasticsearch
Version:	1.0.0
Release:	1%{?dist}
Summary:	Client for Elasticsearch 

Group:		Development/Languages
License:	ASL 2.0
URL:		https://github.com/elasticsearch/elasticsearch-py
Source0:	https://pypi.python.org/packages/source/e/%{tarball_name}/%{tarball_name}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python-devel python-setuptools
Requires:	python-thrift
#Requires:	python-urllib3 >= 1.7
Requires:	python-urllib3 >= 1.5

%description
Low level client for Elasticsearch. It's goal is to provide common ground
for all Elasticsearch-related code in Python. The client's features include:

- Translating basic Python data types to and from json
- Configurable automatic discovery of cluster nodes
- Persistent connections
- Load balancing (with pluggable selection strategy) across all available nodes
- Failed connection penalization (time based - failed connections won't be
  retried until a timeout is reached)
- Thread safety
- Pluggable architecture

%prep
%setup -qn %{tarball_name}-%{version}
%{__rm} -fr %{tarball_name}.egg-info
%{__rm} README
%{__cp} README.rst README 

%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%{python_sitelib}/*
%doc README LICENSE

%changelog
* Mon Feb 24 2014 Romain Acciari <romain.acciari@worldline.com> - 1.0.0-1
- Bump to 1.0.0
- Adapted for CentOS 6

* Thu Dec 19 2013 Daniel Bruno <dbruno@fedoraproject.org> - 0.4.3-4
- Fix broken dependencies

* Wed Dec 11 2013 Daniel Bruno <dbruno@fedoraproject.org> - 0.4.3-3
- Standarizing the spec

* Wed Dec 11 2013 Daniel Bruno <dbruno@fedoraproject.org> - 0.4.3-2
- Fixing lib require

* Tue Nov 26 2013 Daniel Bruno <dbruno@fedoraproject.org> - 0.4.3-1
- First RPM release
