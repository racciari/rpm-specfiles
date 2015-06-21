Name:		nodejs-compat-symlinks
Version:	1.1
Release:	1%{?dist}
Summary:	Compatibility symlinks for Node.js modules
License:	Public Domain
URL:		http://nodejs.tchol.org/
# downloaded from https://github.com/isaacs/node-tap/tarball/9d7cd989c77b39ccd58ce147e2fe86ca5aeafe0e
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Conflicts:	node
Requires:	nodejs

%description
This contains compatibility symlinks for Node modules and applications that
expect Node's binaries and directories to be called "node" instead of "nodejs".

This package and the "node" package cannot be installed at the same time because
many files will conflict.


%package -n nodejs-devel-compat-symlinks
Summary:	Compatibility symlinks to build  Node.js modules
Conflicts:	node,node-devel
Requires:	%{name},nodejs-devel
%description -n nodejs-devel-compat-symlinks
This contains compatibility symlinks to build Node modules and applications that
expect Node's binaries and directories to be called "node" instead of "nodejs".

This package and the "node" package cannot be installed at the same time because
many files will conflict.


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}

ln -s ./nodejs %{buildroot}%{_bindir}/node
ln -s ./nodejs %{buildroot}%{_includedir}/node

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/node

%files -n nodejs-devel-compat-symlinks
%defattr(-,root,root,-)
%{_includedir}/node

%changelog
* Wed Nov 28 2012 Romain Acciari <romain.acciari@openio.io> - 1.1-1
- Add nodejs-devel-compat-symlinks package
* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0-1
- initial package
