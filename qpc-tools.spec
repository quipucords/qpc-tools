%{!?python3_sitelib: %define python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global src_name qpc-tools
%global egg_name qpc_tools
Name: %{src_name}
Version: 0.1.2
Release: 1%{?dist}
Summary: A tool for discovery and inspection of an IT environment. The %{src_name} provides a server base infrastructure to process tasks that discover and inspect remote systems.

Group: Applications/Internet
License: GNU
URL: http://github.com/quipucords/qpc-tools
Source0: http://github.com/quipucords/qpc-tools/archive/copr.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

#Python Version
%if 0%{?el6}
%global pyver 34
%endif
%if 0%{?el7}
%global pyver 36
%endif
%if 0%{?el8}
%global pyver 3
%endif

#Common Requirements
Requires: ansible >= 2.4
%if "%{dist}" != ".el8"
BuildRequires: pandoc
%endif
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
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

%if "%{dist}" == ".el8"
curl -k -SL https://github.com/jgm/pandoc/releases/download/2.7.3/pandoc-2.7.3-linux.tar.gz -o pandoc.tar.gz
tar xvzf pandoc.tar.gz --strip-components 1 -C ~/
make manpage pandoc=~/bin/pandoc
%else
make manpage
%endif

%files
%defattr(-,root,root,-)
%doc README.md AUTHORS.md
%license LICENSE
%{_bindir}/%{src_name}
%{python3_sitelib}/%{egg_name}
%{python3_sitelib}/%{egg_name}-%{version}-py3.?.egg-info/

%changelog
* Thu Jun 27 2019 Cody Myers <cmyers@redhat.com> 0.1.2
- Creating the qpc-tools as a spec
