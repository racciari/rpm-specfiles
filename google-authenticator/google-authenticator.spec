Name:		google-authenticator
Version:	1.0
Release:	1%{?dist}
Summary:	One-time passcode support using open standards

Group:		System Environment/Base
License:	ASL 2.0
URL:		https://github.com/google/google-authenticator/
Source0:	https://github.com/google/google-authenticator/archive/master.tar.gz

BuildRequires:	autoconf,automake,libtool
BuildRequires:	pam-devel
%if 0%{?fedora}
BuildRequires:	qrencode-devel
%endif
Requires:	pam

%description
The Google Authenticator package contains a pluggable authentication
module (PAM) which allows login using one-time passcodes conforming to
the open standards developed by the Initiative for Open Authentication
(OATH) (which is unrelated to OAuth).

Passcode generators are available (separately) for several mobile
platforms.

These implementations support the HMAC-Based One-time Password (HOTP)
algorithm specified in RFC 4226 and the Time-based One-time Password
(TOTP) algorithm currently in draft.


%prep
%setup -q -n %{name}-master/libpam
autoreconf -iv


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%{_bindir}/google-authenticator
%{_libdir}/security/*
%{_defaultdocdir}/google-authenticator
%doc FILEFORMAT README totp.html


%changelog
* Mon Jun 01 2015 - 1.0-1 - Romain Acciari <romain.acciari@openio.io>
- Initial release
