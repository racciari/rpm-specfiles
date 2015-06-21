%global with_python3 0%{?fedora} >= 17

Name:           python-pyro 
Version:        4.12
Release:        1%{?dist}
Summary:        PYthon Remote Objects

Group:          Development/Languages
License:        MIT 
URL:            http://packages.python.org/Pyro4/ 
Source0:        http://pypi.python.org/packages/source/P/Pyro4/Pyro4-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch 
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: /usr/bin/2to3
%endif # if with_python3

%description
Pyro provides an object-oriented form of RPC. You can use Pyro within a
single system but also use it for IPC. For those that are familiar with
Java, Pyro resembles Java's Remote Method Invocation (RMI). It is less
similar to CORBA - which is a system- and language independent Distributed
Object Technology and has much more to offer than Pyro or RMI.

%if 0%{?with_python3}
%package -n python3-pyro
Summary:        Python Remote Objects
Group:          Development/Languages
%description -n python3-pyro
Pyro provides an object-oriented form of RPC. You can use Pyro within a
single system but also use it for IPC. For those that are familiar with
Java, Pyro resembles Java's Remote Method Invocation (RMI). It is less
similar to CORBA - which is a system- and language independent Distributed
Object Technology and has much more to offer than Pyro or RMI.
%endif # with_python3

%prep
%setup -q -n Pyro4-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find examples -type f -exec sed -i 's/\r//' {} \;
find docs -type f -exec sed -i 's/\r//' {} \;
sed -i 's/\r//' README.txt LICENSE
chmod -x examples/echoserver/{Readme.txt,client.py}
chmod -x examples/gui_eventloop/{gui_threads.py,gui_nothreads.py}
#chmod -x examples/maxsize/Readme.txt


%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find examples -type f -exec sed -i 's/\r//' {} \;
find docs -type f -exec sed -i 's/\r//' {} \;
sed -i 's/\r//' README.txt LICENSE
chmod -x examples/echoserver/{Readme.txt,client.py}
chmod -x examples/gui_eventloop/{gui_threads.py,gui_nothreads.py}
#chmod -x examples/maxsize/Readme.txt
popd
%endif # with_python3

%files
%defattr(-,root,root,-)
%doc docs/* examples README.txt LICENSE
%{python_sitelib}/Pyro4
%{python_sitelib}/Pyro4-*.egg-info

%if 0%{?with_python3}
%files -n python3-pyro
%defattr(-,root,root,-)
%doc docs/* examples README.txt LICENSE
%{python3_sitelib}/Pyro4
%{python3_sitelib}/Pyro4-*.egg-info
%endif

%changelog
* Fri Oct 25 2013 Romain Acciari <romain.acciari@openio.io> 4.12-1
- Downgrade to 4.12 for Shinken compatibility

* Mon Sep 24 2012 David Hannequin <david.hannequin@gmail.com> 4.14-2
- adapt to el6

* Wed Aug 22 2012 David Hannequin <david.hannequin@gmail.com> 4.14-1
- Update from upstream
- Fix url 

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 4.9-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 1 2011 David Hannequin <david.hannequin@gmail.com> 4.9-1
- Update from upstream

* Wed Mar 13 2011 David Hannequin <david.hannequin@gmail.com> 4.3-2
- Python 3 support (thanks Haïkel Guémar)

* Sat Mar 9 2011 David Hannequin <david.hannequin@gmail.com> 4.3-1
- Update from upstream

* Sun Jan 16 2011 David Hannequin <david.hannequin@gmail.com> 4.2-1
- Update from upstream

* Tue Oct 12 2010 David Hannequin <david.hannequin@gmail.com> 4.0-3
- package for Fedora 13 

* Mon Oct 11 2010 David Hannequin <david.hannequin@gmail.com> 4.0-2
- Delete clean section
- Add license file

* Tue Aug 03 2010 David Hannequin <david.hannequin@gmail.com> 4.0-1
- First release to Fedora
