%global shortname common

Name:           jgoodies-common
Version:        1.8.0
Release:        1%{?dist}
Summary:        Common library shared by JGoodies libraries and applications

Group:          Development/Libraries
License:        BSD
URL:            http://www.jgoodies.com/
Source0:        http://www.jgoodies.com/download/libraries/%{shortname}/%{name}-%(tr "." "_" <<<%{version}).zip

# fontconfig and DejaVu fonts needed for tests
BuildRequires:  dejavu-sans-fonts
BuildRequires:  fontconfig
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-dependency-plugin
Requires:       jpackage-utils
BuildArch:      noarch

%description
The JGoodies Common library provides convenience code for other JGoodies
libraries and applications.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q

# Unzip source and test files from provided JARs
mkdir -p src/main/java/ src/test/java/
pushd src/main/java/
jar -xf ../../../%{name}-%{version}-sources.jar
popd
pushd src/test/java/
jar -xf ../../../%{name}-%{version}-tests.jar
popd

# Delete prebuild JARs
find -name "*.jar" -exec rm {} \;

# Remove DOS line endings
for file in LICENSE.txt RELEASE-NOTES.txt; do
  sed 's|\r||g' $file > $file.new && \
  touch -r $file $file.new && \
  mv $file.new $file
done

%mvn_file :%{name} %{name} %{name}


%build
%mvn_build


%install
%mvn_install


%files -f .mfiles
%doc LICENSE.txt README.html RELEASE-NOTES.txt


%files javadoc -f .mfiles-javadoc


%changelog
* Fri Jun 13 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.7.0-2
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 12 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Fri Aug 16 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.6.0-3
- Update for newer guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 11 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4.0-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 01 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 03 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Wed Feb 15 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 03 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Sat Feb 19 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.1.1-2
- Remove obsolete clean section and BuildRoot tag

* Wed Feb 09 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.1.1-1
- Initial RPM release
