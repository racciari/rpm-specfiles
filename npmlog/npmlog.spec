Name:		npmlog
Version:	20121109
Release:	1%{?dist}
Summary:	The logger util that npm uses.

Group:		nodejs
License:	BSD
URL:		https://github.com/isaacs/npmlog
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
Requires:	npm

%description
The logger util that npm uses.

This logger is very basic. It does the logging for npm. It supports custom
levels and colored output.

By default, logs are written to stderr. If you want to send log messages to
outputs other than streams, then you can change the log.stream member, or you
can just listen to the events that it emits, and do whatever you want with them.


%prep
%setup -q -n npmlog-master


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT/usr/lib/npm/lib
%{__install} log.js $RPM_BUILD_ROOT/usr/lib/npm/lib/



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README.md
/usr/lib/npm/lib/*


%changelog
* Fri Nov 09 2012 - 20121109-1 - Romain Acciari
- Initial release
