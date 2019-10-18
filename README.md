# qpc-tools

Installs the Quipucords server and CLI.  Quipucords is a tool for discovery, inspection, collection, deduplication, and reporting on an IT environment.

This *README* file contains information about the installation and development of qpc-tools, as well as instructions about where to find basic usage, known issues, and best practices information.

- [Introduction to qpc-tools](#intro)
- [Requirements and Assumptions](#requirements)
- [Installation](#installation)
- [Development](#development)
- [Test](#test)
- [Issues](#issues)
- [Authors](#authors)
- [Copyright and License](#copyright)


# <a name="intro"></a> Introduction to qpc-tools
The qpc-tools package is a bash script that utilizes Ansible to install both the Quipucords server and CLI.


# <a name="requirements"></a> Requirements and Assumptions
Before installing qpc-tools on a system, review the following guidelines about installing and running Quipucords and qpc-tools:

 - qpc-tools is written to run on RHEL or CentOS servers.

# <a name="installation"></a> Installation
To work with the qpc-tools, begin by cloning the repository.

```
git clone git@github.com:quipucords/qpc-tools.git
cd qpc-tools/install
./qpc-tools
```

# <a name="development"></a> Development
To develop the qpc-tools, begin by cloning the repository.
```
git clone git@github.com:quipucords/qpc-tools.git
```
# <a name="test"></a> Test
There are various options testing your changes to the installation scripts. You can test scripts from this repository or an official build.

## Setup
- First obtain all the required repositories
```
git clone git@github.com:quipucords/quipucords.git
git clone git@github.com:quipucords/quipucords-ui.git
git clone git@github.com:quipucords/qpc-tools.git
```

## Testing local installation scripts
This method is used when you are testing installation scripts that have not been released.

### Testing online installation
To test your local scripts on all supported OS's run the following.
```
make setup-local-online
make test-all
```

If you make changes to the installation scripts and want to test them you can run:
```
make refresh
```
There is no need to restart the VM.

### Testing offline installation
To build the docker image, download the `qpc` client and test with the local install scripts on all supported OS's, run the following:
```
make setup-local-offline server_source=release cli_version=0.9.0 server_version=0.9.0
make test-all
```
**Options:**
- `server_source`
  - Contains `local` or `release` value. Defaults to `release`. Supply `local` to build the server docker image from a local quipucords repository, or `release` to use release server docker image.
- `cli_version`
  - Contains the released version of the `qpc` client. Defaults to `latest`. Supply the client version number you want to use.
- `server_version`
  - Contains Quipucords server version number. Required if `server_source` is `local`. If `server_source` is `release`, then defaults to `latest`. Supply the server version number you want to use.

If you make changes to the installation scripts and want to test them you can run:
```
make refresh
```
There is no need to restart the VM.

**Warning:** If you are switching from doing an offline test to online, then you should run `make clean` on the qpc-tools repository folder before starting the online installation.

## Testing released installation scripts
This method is used when you are testing installation scripts that have been released.  They will be available on GitHub.

### Testing online installation
To test the release scripts on all supported OS's, run the following.
```
make setup-release-online tools_version=0.1.1
make test-all
```
**Options:**
- `tools_version`
  - Contains the released version of the `qpc-tools`. Defaults to `latest`. Supply the qpc-tools version number you want to use.

### Testing offline installation
To test the release scripts on all supported OS's, run the following. This command will download Quipucords server docker image, qpc-tools, `qpc` client and copy them to OS specific folders.
```
make setup-release-offline tools_version=0.1.1 cli_version=0.9.0 server_version=0.9.0
make test-all
```
**Options:**
- `tools_version`
  - Contains the released version of the `qpc-tools`. Defaults to `latest`. Supply the qpc-tools version number you want to use.
- `cli_version`
  - Contains the released version of the `qpc` client. Defaults to `latest`. Supply the client version number you want to use.
- `server_version`
  - Contains Quipucords server version number. Defaults to `latest`. Supply the server version number you want to use.

## Configuring Virtual Machines
The above `test-all` command will perform a  `vagrant ssh`.  If you have no configuration help, then you can simply run `qpc-tools`.

### Optional Secret Configuration
Create or obtain a tarball named `tools_config.tar.gz`.  The files in this tarball will automatically be copied inside the VMs mapped volumes.  If you are testing rhel6 or rhel7 and have internal repositories, your `tools_config.tar.gz` should have the following structure:
```
- config
    - rhel6
        - rhel 6 repository files
    - rhel7
        - rhel 7 repository files
    - rhel8
        - rhel 8 repository files
```

The repository files will be copied to the `/etc/yum.repos.d/` directory in the virtual machine.

## Vagrant: Testing Online Installation
To test online installation, do the following:
```
clear;cd /qpc_tools;sudo su
make setup
make install-local-tools --or-- make install-release-tools
qpc-tools server install
qpc-tools cli install
```
Note:
 - Optionally run any secret post install scripts you included in `tools_config.tar.gz`

## Vagrant: Testing Offline Installation

To test offline installation for RHEL 6/7/8 or CentOS 6/7, do the following (with internet connectivity):

```
clear;cd /qpc_tools;sudo su
make setup
make offline-prep
make install-local-tools --or-- make install-release-tools
# Disconnect from the network
qpc-tools server install --offline-files /qpc_tools/install/packages
qpc-tools cli install --ofline-files /qpc_tools/install/packages
```

Note:
 - Optionally run any secret post install scripts you included in `tools_config.tar.gz`

 ## Creating the man page
 After installing [pandoc](https://pandoc.org/installing.html) locally, run the following command:

```
 make manpage
 cd install; man ./qpc-tools.1
```

# <a name="issues"></a> Issues
To report bugs for qpc-tools [open issues](https://github.com/quipucords/qpc-tools/issues) against this repository in Github. Complete the issue template when opening a new bug to improve investigation and resolution time.


# <a name="authors"></a> Authors
Authorship and current maintainer information can be found in [AUTHORS](AUTHORS.md)


# <a name="copyright"></a> Copyright and License
Copyright 2019, Red Hat, Inc.

qpc-tools is released under the [GNU Public License version 3](LICENSE)
