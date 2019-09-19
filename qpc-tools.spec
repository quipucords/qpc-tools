%global src_name qpc-tools
Name: %{src_name}
Version: 0.1.2
Release: 1%{?dist}
Summary: A tool for discovery and inspection of an IT environment. The %{src_name} provides a server base infrastructure to process tasks that discover and inspect remote systems.

Group: Applications/Internet
License: GNU
URL: http://github.com/quipucords/qpc-tools
Source0: %{src_name}-%{version}.tar.gz

BuildArch: noarch
#Common Requirements
Requires: ansible >= 2.4
%if "%{dist}" != ".el8"
BuildRequires: pandoc
%endif

%description
A tool for discovery and inspection of an IT environment. The %{src_name} provides a server base infrastructure to process tasks that discover and inspect remote systems.

%prep
%setup -q

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
pushd %{_builddir}/%{src_name}-*
%if "%{dist}" == ".el8"
curl -k -SL https://github.com/jgm/pandoc/releases/download/2.7.3/pandoc-2.7.3-linux.tar.gz -o pandoc.tar.gz
tar xvzf pandoc.tar.gz --strip-components 1 -C ~/
make manpage pandoc=~/bin/pandoc
%else
make manpage
%endif
sed -i 's?PLAYBOOKPATH=""?PLAYBOOKPATH="%{_libdir}/%{src_name}-%{version}/install/"?g' install/%{src_name}
sed -i 's/BUILD_VERSION_PLACEHOLDER/%{version}/g' install/%{src_name}
cp -rf install/%{src_name} %{buildroot}%{_bindir}/%{src_name}
popd
cp -rf %{_builddir}/%{src_name}-* %{buildroot}%{_libdir}/%{src_name}-%{version}
chmod 755 %{buildroot}%{_bindir}/%{src_name}

install -D -p -m 644 %{buildroot}%{_libdir}/%{src_name}-%{version}/docs/%{src_name}.1 %{buildroot}%{_mandir}/man1/%{src_name}.1

%files
%defattr(-,root,root,-)
%doc README.md AUTHORS.md
%license LICENSE
/%{_libdir}/%{src_name}-%{version}
%{_mandir}/man1/%{src_name}.1.gz
%{_bindir}/%{src_name}

%changelog
* Thu Jun 27 2019 Cody Myers <cmyers@redhat.com> 0.1.2
- Creating the installer as a spec
