Name:       npm
Version:    1.1.65
Release:    2%{?dist}
Summary:    Node.js Package Manager
License:    MIT
Group:      Development/Tools
URL:        http://npmjs.org/
Source0:    http://registry.npmjs.org/npm/-/npm-%{version}.tgz
# forces npm to keep config files in /etc instead of /usr/etc
Source1:    npmrc
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires: nodejs-devel

%if !(0%{?fedora} >= 17)
Requires:   nodejs nodejs-devel nodejs-waf gcc gcc-c++
Requires:   nodejs-nopt nodejs-proto-list nodejs-slide-flow-control
Requires:   nodejs-fast-list nodejs-inherits nodejs-mkdirp nodejs-read
Requires:   nodejs-uid-number nodejs-fstream-npm nodejs-archy nodejs-chownr

Requires:   node-gyp >= 0.3.8
Requires:   nodejs-abbrev >= 1.0.3
Requires:   nodejs-rimraf >= 1.0.9
Requires:   nodejs-node-uuid >= 1.3.3
Requires:   nodejs-graceful-fs >= 1.1.8
Requires:   nodejs-request >= 2.9.153
Requires:   nodejs-semver >= 1.0.13
Requires:   nodejs-block-stream >= 0.0.5
Requires:   nodejs-lru-cache >= 1.0.6
Requires:   nodejs-ini >= 1.0.1
Requires:   nodejs-minimatch >= 0.2.2
Requires:   nodejs-which >= 1.0.5
Requires:   nodejs-fstream >= 0.1.17
Requires:   nodejs-tar >= 0.1.13
%endif

%description
npm is a package manager for node.js. You can use it to install and publish your
node programs. It manages dependencies and does other cool stuff.

%prep
%setup -q -n npm

%nodejs_fixshebang bin/npm-cli.js cli.js bin/read-package-json.js


%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/npm/bin
cp -pr %{SOURCE1} lib man cli.js package.json %{buildroot}%{nodejs_libdir}/npm/
cp -p bin/*.js %{buildroot}%{nodejs_libdir}/npm/bin/

mkdir -p %{buildroot}%{_bindir}
ln -s ../lib/nodejs/npm/bin/npm-cli.js %{buildroot}%{_bindir}/npm

# ghosted global config files
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/npmrc
touch %{buildroot}%{_sysconfdir}/npmignore

# Install required node modules
cp -pr node_modules %{buildroot}%{nodejs_libdir}/npm/node_modules

# install to mandir
mkdir -p %{buildroot}%{_datadir}
cp -pr man %{buildroot}%{_datadir}/

# prefix all manpages with "npm-"
pushd %{buildroot}%{_datadir}/man
for dir in *; do
    pushd $dir
    for page in *; do
        if [[ $page != npm* ]]; then
            mv $page npm-$page
        fi
    done
    popd
done
popd


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{nodejs_libdir}/npm
%{nodejs_libdir}/npm/bin
%{nodejs_libdir}/npm/cli.js
%{nodejs_libdir}/npm/lib
%{nodejs_libdir}/npm/man
%{nodejs_libdir}/npm/node_modules
%{nodejs_libdir}/npm/package.json
%config %{nodejs_libdir}/npm/npmrc
%ghost %{_sysconfdir}/npmrc
%ghost %{_sysconfdir}/npmignore
%{_bindir}/npm
%{_mandir}/*
%doc AUTHORS doc/* html README.md LICENSE

%changelog
* Wed Nov 21 2012 Romain Acciari <romain.acciari@openio.io> - 1.1.65-2
- Fix npm node_modules

* Fri Nov 09 2012 Romain Acciari <romain.acciari@openio.io> - 1.1.65-1
- New upstream release 1.1.65

* Wed May 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.19-1
- New upstream release 1.1.19

* Wed May 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.19-1
- New upstream release 1.1.19

* Wed Apr 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.18-1
- New upstream release 1.1.18

* Fri Apr 06 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.16-1
- New upstream release 1.1.16

* Mon Apr 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.15-1
- New upstream release 1.1.15

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.14-1
- New upstream release 1.1.14

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.13-2
- new dependencies fstream-npm, uid-number, and fstream-ignore (indirectly)

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.13-1
- new upstream release 1.1.13

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.12-1
- new upstream release 1.1.12

* Thu Mar 15 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.9-1
- new upstream release 1.1.9

* Sun Mar 04 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.4-1
- new upstream release 1.1.4

* Sat Feb 25 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.2-1
- new upstream release 1.1.2

* Sat Feb 11 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.1-2
- fix node_modules symlink

* Thu Feb 09 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.1-1
- new upstream release 1.1.1

* Sun Jan 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-2.3
- new upstream release 1.1.0-3

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-2.2
- missing Group field for EL5

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-1.2
- new upstream release 1.1.0-2

* Tue Nov 17 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.106-1
- new upstream release 1.0.106
- ship manpages again

* Thu Nov 10 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.105-1
- new upstream release 1.0.105
- use relative symlinks instead of absolute
- fixes /usr/bin/npm symlink on i686

* Mon Nov 07 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.104-1
- new upstream release 1.0.104
- adds node 0.6 support

* Wed Oct 26 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.101-2
- missing Requires on nodejs-request
- Require compilers too so native modules build properly

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.101-1
- new upstream release
- use symlink /usr/lib/node_modules -> /usr/lib/nodejs instead of patching

* Thu Aug 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.26-2
- rebuilt with fixed nodejs_fixshebang macro from nodejs-devel-0.4.11-3

* Tue Aug 23 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.26-1
- initial package
