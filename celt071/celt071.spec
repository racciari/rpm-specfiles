Name:           celt071
Version:        0.7.1
Release:        8%{?dist}
Summary:        An audio codec for use in low-delay speech and audio communication

Group:          System Environment/Libraries
License:        BSD and GPLv2+
# Files without license header are confirmed to be BSD. Will be fixed in later release
# http://lists.xiph.org/pipermail/celt-dev/2009-February/000063.html
URL:            http://www.celt-codec.org/
Source0:        http://downloads.us.xiph.org/releases/celt/celt-%{version}.tar.gz
Source1:        %{name}.pc.in
Patch0:         %{name}-append-version-suffix.patch
BuildRequires:  libogg-devel
BuildRequires:  libtool
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
CELT (Constrained Energy Lapped Transform) is an ultra-low delay audio
codec designed for realtime transmission of high quality speech and audio.
This is meant to close the gap between traditional speech codecs
(such as Speex) and traditional audio codecs (such as Vorbis).

The CELT bitstream format is not yet stable, this package is a special
version of 0.7.1 that has the same bitstream format, but symbols and files
renamed from 'celt*' to 'celt071*' so that it is parallel installable with
the normal celt for packages requiring this particular bitstream format.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: libogg-devel
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n celt-%{version}
cp %{SOURCE1} .
%patch0 -p1
autoreconf -f -i

%build
%configure --disable-static
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm %{buildroot}/%{_libdir}/libcelt071.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_bindir}/celtenc071
%{_bindir}/celtdec071
%{_libdir}/libcelt071.so.0
%{_libdir}/libcelt071.so.0.0.0

%files devel
%defattr(-,root,root,-)
%doc COPYING README
%{_includedir}/celt071
%{_libdir}/pkgconfig/celt071.pc
%{_libdir}/libcelt071.so

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 27 2013 Christian Krause <chkr@fedoraproject.org> - 0.7.1-7
- Build fix (rhbz#992049)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Apr  3 2011 Andreas Osowski <th0br0@mkdir.name> - 0.7.1-2
- Fixed %%{buildroot} usage
- Added missing BuildRequire: libtool
* Sat Oct  9 2010 Andreas Osowski <th0br0@mkdir.name> - 0.7.1-1
- First fedora package, based on celt051
