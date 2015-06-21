%global shortname looks

Name:           jgoodies-looks
Version:        2.6.0
Release:        1%{?dist}
Summary:        Free high-fidelity Windows and multi-platform appearance

Group:          Development/Libraries
License:        BSD
URL:            http://www.jgoodies.com/freeware/looks/
Source0:        http://www.jgoodies.com/download/libraries/%{shortname}/%{name}-%(tr "." "_" <<<%{version}).zip

# Fontconfig and DejaVu fonts needed for tests
BuildRequires:  dejavu-sans-fonts
BuildRequires:  fontconfig
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jgoodies-common >= 1.8.0
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-dependency-plugin
Requires:       java >= 1:1.6.0
Requires:       jgoodies-common >= 1.8.0
Requires:       jpackage-utils
# JGoodies Looks <= 2.4.2 doesn't provide demo jars anymore
Provides:       %{name}-demo = %{version}-%{release}
Obsoletes:      %{name}-demo < 2.4.2
BuildArch:      noarch

%description
The JGoodies look&feels make your Swing applications and applets look better.
They have been optimized for readability, precise micro-design and usability.


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

# Move the resources into a "resources" directory so they end up packaged
# properly
mkdir -p src/main/resources/com/jgoodies/looks/plastic/
mv src/main/java/com/jgoodies/looks/plastic/icons/ src/main/resources/com/jgoodies/looks/plastic/
mkdir -p src/main/resources/com/jgoodies/looks/common
mv src/main/java/com/jgoodies/looks/common/*.png src/main/resources/com/jgoodies/looks/common/

# Delete prebuild JARs
find -name "*.jar" -exec rm {} \;

# Fix wrong end-of-line encoding
for file in LICENSE.txt RELEASE-NOTES.txt; do
  sed -i.orig "s/\r//" $file && \
  touch -r $file.orig $file && \
  rm $file.orig
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
* Fri Jun 13 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 16 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.5.3-3
- Update for newer guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 11 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.5.3-1
- Update to 2.5.3

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.5.2-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 01 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2
- Drop patch jgoodies-looks-2.5.1-build.patch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 19 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.5.1-2
- Include missing resources in JAR file (reported and fixed by Mary Ellen
  Foster)

* Fri May 04 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1

* Thu Feb 16 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0
- Add missing look jars

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.4.2-2
- Add necessary Provides/Obsoletes since there is no more jgoodies-looks-demo
  subpackage

* Fri Dec 16 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2
- Spec cleanup

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon May 19 2008 Mary Ellen Foster <mefoster at gmail.com> 1.2.0-1
- Update to 1.2.0

* Tue Oct 16 2007 Mary Ellen Foster <mefoster at gmail.com> 1.1.0-2
- Fix encoding on HTML files
- Use empty CLASSPATH when building
- Fix indentation in spec file

* Wed Sep  5 2007 Mary Ellen Foster <mefoster at gmail.com> 1.1.0-1
- Initial version for Fedora, based on JPackage spec by Eric Lavarde
