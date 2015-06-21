%global gem_name listen
%global rubyabi 1.8.7
%global gem_dir /usr/lib/ruby/gems/1.8/gems

Name:		graphene
Version:	20140310
Release:	1%{?dist}
Summary:	Realtime dashboard and graphing toolkit based on D3 and Backbone

Group:		Applications/Internet
License:	MIT
URL:		https://github.com/jondot/graphene
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

#BuildRequires:	
#BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby
BuildRequires:	rubygems-devel >= 1.3.6
#BuildRequires:	rubygem(rspec)
#BuildRequires:	rubygem(rb-inotify)
#Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby
Requires:	ruby(rubygems) >= 1.3.6
Provides:	rubygem(%{gem_name}) = %{version}
#Requires:	rubygem-uglifier,rubygem-coffee-script,rubygem-sass-rails,rubygem-guard-sprockets,rubygem-listen

%description
Graphene is a realtime dashboard & graphing toolkit based on D3 and Backbone.
It was made to offer a very aesthetic realtime dashboard that lives on top
of Graphite (but could be tailored to any back end, eventually).


%prep
%setup -q
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0}


%build
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc



%changelog
* Mon Mar 10 2014 Romain Acciari <romain.acciari@openio.io> 20140310-1
- Initial release
