%global stream_name quipucords
%global ver 0.1.2
####
%global src_name %{stream_name}-installer
%global egg_name %{stream_name}_installer
Name: %{src_name}
Version: %{ver}
Release: 1%{?dist}
Summary: A tool for discovery and inspection of an IT environment. The %{src_name} provides a server base infrastructure to process tasks that discover and inspect remote systems.

Group: Applications/Internet
License: GNU
URL: http://github.com/quipucords/quipucords
Source0: %{src_name}-%{version}.tar.gz

BuildArch: noarch
#Common Requirements
Requires: ansible >= 2.4
%if "%{stream_name}" == "quipucords"
BuildRequires: pandoc
%endif

# Discovery (Downstream)
%if "%{stream_name}" == "discovery"
# Downstream rpmbuilder bombs when there are no BuildRequires
BuildRequires: ansible
Requires: podman
%endif


%description
A tool for discovery and inspection of an IT environment. The %{src_name} provides a server base infrastructure to process tasks that discover and inspect remote systems.

%prep
%setup -q

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
pushd %{_builddir}/%{src_name}-*
sed -i 's?PLAYBOOKPATH=""?PLAYBOOKPATH="%{_libdir}/%{src_name}-%{version}/install/"?g' install/%{src_name}
sed -i 's/BUILD_VERSION_PLACEHOLDER/%{version}/g' install/%{src_name}
cp -rf install/%{src_name} %{buildroot}%{_bindir}/%{src_name}
%if "%{stream_name}" == "quipucords"
make manpage
%endif
popd
cp -rf %{_builddir}/%{src_name}-* %{buildroot}%{_libdir}/%{src_name}-%{version}
chmod 755 %{buildroot}%{_bindir}/%{src_name}

install -D -p -m 644 %{buildroot}%{_libdir}/%{src_name}-%{version}/install/%{src_name}.1 %{buildroot}%{_mandir}/man1/%{src_name}.1

%files
%defattr(-,root,root,-)
%doc README.md AUTHORS.md
%license LICENSE
/%{_libdir}/%{src_name}-%{version}
%{_mandir}/man1/%{src_name}.1.gz
%{_bindir}/%{src_name}

%changelog
* Thu Jun 27 2019 Cody Myers <cmyers@redhat.com> 0.9.0
- Creating the installer as a spec
