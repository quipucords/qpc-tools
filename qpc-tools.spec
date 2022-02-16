%{!?python3_sitelib: %define python3_sitelib %(%{__python3} -c "import site; print(site.getsitepackages()[0])")}
%global src_name qpc-tools
%global egg_name qpc_tools
Name: %{src_name}
Version: 0.3.0
Release: 1%{?dist}
Summary: A tool for discovery and inspection of an IT environment. The %{src_name} provides a server base infrastructure to process tasks that discover and inspect remote systems.

Group: Applications/Internet
License: GNU
URL: http://github.com/quipucords/qpc-tools
Source0: http://github.com/quipucords/qpc-tools/archive/refs/heads/master.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

%if 0%{?el7}
%global pyver 36
%else
%global pyver 3
%endif

BuildRequires: make
BuildRequires: pandoc
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
Requires: ansible >= 2.4
Requires: python%{pyver}

%description
A tool for discovery and inspection of an IT environment. The %{src_name} provides a server base infrastructure to process tasks that discover and inspect remote systems.

%prep
%setup -q

%build
make manifest
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
make manpage
install -D -p -m 644 docs/qpc-tools.1 %{buildroot}%{_mandir}/man1/qpc-tools.1

%files
%defattr(-,root,root,-)
%doc README.md AUTHORS.md
%license LICENSE
%{_bindir}/%{src_name}
%{python3_sitelib}/%{egg_name}
%{python3_sitelib}/%{egg_name}-%{version}-py%{python3_version}.egg-info/
%{_mandir}/man1/%{src_name}.1.gz

%changelog
* Wed Feb 16 2022 Bruno Ciconelle <bciconel@redhat.com> 0.3.0
- Add support for latest fedora and add small improvements to specfile
- Improve podman-based installation method
- Bump postgres version to 14.1
- Update supported python versions to 3.6 ~ 3.9
* Fri Jan 24 2020 Kevan Holdaway <kholdawa@redhat.com> 0.2.5
- Change master branch version to 0.2.5
* Fri Jan 24 2020 Kevan Holdaway <kholdawa@redhat.com> 0.2.4
- Change master branch version to 0.2.4
- Set have_epel default to false in CLI install playbook
* Thu Dec 12 2019 Cody Myers <cmyers@redhat.com> 0.2.3
- Update version for master <cmyers@redhat.com>
- Add suport for Centos8 <kholdawa@redhat.com>
- Fixed bad ansible condition in registry authentication <cmyers@redhat.com>
* Tue Dec 03 2019 Kevan Holdaway <kholdawa@redhat.com> 0.2.2
- Update version for master <kholdawa@redhat.com>
- Turn off server SSL validation for quipucords server image <kholdawa@redhat.com>
- Add args to support installing from satellite downstream <cmyers@redhat.com>
* Thu Nov 07 2019 Cody Myers <cmyers@redhat.com> 0.2.1
- fix unintentional default var overwrite <cmyers@redhat.com>
- Remove registry user from required args <cmyers@redhat.com>
* Thu Oct 24 2019 Cody Myers <cmyers@redhat.com> 0.2.0
- transitioned to a python client <kholdawa@redhat.com>
- added for support RHEL8 <dtoirov@redhat.com>
- added support for Podman on RHEL8 & RHEL/Centos7 <dtoirov@redhat.com>
- added support for upgrading from docker to podman <kholdawa@redhat.com>
- converted the installation script into an RPM <cmyers@redhat.com>
- renamed the installer from quipucords-installer to qpc-tools <cmyers@redhat.com>
- added a role for Redhat Registry authentication <cmyers@redhat.com>
- added prompts for passwords & Redhat Registry username <aaiken@redhat.com>
- handled advanced arguments for ansible-extras <aaiken@redhat.com>
