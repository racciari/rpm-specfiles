Name:		librdkafka
Version:	0.8.6
Release:	1%{?dist}
Summary:	The Apache Kafka C library

Group:		Development/Libraries/C and C++
License:	BSD-2-Clause
URL:		https://github.com/edenhill/librdkafka
Source0:	https://github.com/edenhill/librdkafka/archive/%{version}.tar.gz
Patch0:		librdkafka-fix-signedness.patch

BuildRequires:	zlib-devel 
#BuildRequires:	libstdc++-devel gcc >= 4.1 gcc-c++
#Requires:	

%description
librdkafka is a C library implementation of the Apache Kafka protocol,
containing both Producer and Consumer support. It was designed with
message delivery reliability and high performance in mind, current
figures exceed 800000 msgs/second for the producer and 3 million
msgs/second for the consumer.


%package	devel
Summary:	The Apache Kafka C library (Development Environment)
Group:		Development/Libraries/C and C++
Requires:	%{name} = %{version}

%description	devel
librdkafka is a C library implementation of the Apache Kafka protocol,
containing both Producer and Consumer support.

This package contains headers and libraries required to build applications
using librdkafka.


%prep
%setup -q
%patch0 -p1


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%{_libdir}/*
%doc README.md CONFIGURATION.md INTRODUCTION.md
%doc LICENSE LICENSE.pycrc LICENSE.snappy

%files devel
%{_includedir}/librdkafka


%changelog
* Thu Jun 04 2015 Romain Acciari <romain.acciari@openio.io> 0.8.6-1
- New release
- Fix: Fixed signedness to silence gcc-5 (issue #277)
* Tue Feb 03 2015 Romain Acciari <romain.acciari@openio.io> 0.8.5-1
- Initial release
