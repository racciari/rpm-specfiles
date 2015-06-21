Name:		redjs
Version:	20131220
Release:	1%{?dist}
Summary:	Single page S3 browser in JS
BuildArch:	noarch

Group:		HoneyComb
License:	WorldLine
URL:		http://www.redcurrant.io/
Source0:	%{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
Requires:	httpd

%description
Single page S3 browser in JS.


%prep
%setup -q


%build


%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}/var/www/html/redjs
%{__cp} -aT . %{buildroot}/var/www/html/redjs/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/var/www/html/redjs


%changelog
* Fri Dec 20 2013 - 20131220-1 - Romain Acciari
- Initial release
