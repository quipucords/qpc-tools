# Features
- [Issue 67](https://github.com/quipucords/quipucords-installer/issues/67) - Create Ansible roles to install and start podman
- [Issue 95](https://github.com/quipucords/quipucords-installer/issues/95) - Support Podman on quipucords server install for  RHEL/CentOS 7
- [Issue 109](https://github.com/quipucords/quipucords-installer/issues/109) - Upgrade a quipucords docker installation to Podman for RHEL/CentOS 7
- [Issue 16](https://github.com/quipucords/quipucords-installer/issues/16) - Support automated installation on RHEL 8
- [Issue 87](https://github.com/quipucords/quipucords-installer/issues/87) - Change the default port of gunicorn for Podman
- [Issue 68](https://github.com/quipucords/quipucords-installer/issues/68) - Modify installer to reuse roles and more clearly document installation flows
- [Issue 38](https://github.com/quipucords/quipucords-installer/issues/38) - Break quipucords installer ansible roles
- [Issue 89](https://github.com/quipucords/quipucords-installer/issues/89) - Add ability to change username/password of django server during installation
- [Issue 12](https://github.com/quipucords/quipucords-installer/issues/12) - Convert the installation upstream script to an RPM
- [Issue 80](https://github.com/quipucords/quipucords-installer/issues/80) - Create a man page for the installation rpm
- [Issue 92](https://github.com/quipucords/quipucords-installer/issues/92) - Configure spec file to build a RHEL8 rpm
- [Issue 31](https://github.com/quipucords/quipucords-installer/issues/31) - Imporve makefile automation for testing the installation
- [Issue 3](https://github.com/quipucords/qpc-tools/issues/3) - Rename the quipucords-installer to qpc-tools since eventually this may handle more than install
- [Issue 7](https://github.com/quipucords/qpc-tools/issues/7) - Move installation packages default directory to the quipucords directory and allow overriding default
- [Issue 13](https://github.com/quipucords/qpc-tools/issues/13) - Define custom facing python command line args
- [Issue 23](https://github.com/quipucords/qpc-tools/issues/23) - Update CLI configure to use the host/port args
- [Issue 28](https://github.com/quipucords/qpc-tools/issues/28) - qpc-tools install command should prompt for passwords
- [Issue 30](https://github.com/quipucords/qpc-tools/issues/30) - Add a role for Redhat Registry Authentication
- [Issue 38](https://github.com/quipucords/qpc-tools/issues/38) - Add new server playbook vars for downstream
- [Issue 41](https://github.com/quipucords/qpc-tools/issues/41) - Prompt for registry username if not provided
- [Issue 49](https://github.com/quipucords/qpc-tools/issues/49) - Add logging for subprocess stderr, ansible command & cancel install

# Bugs
- [Issue 15](https://github.com/quipucords/quipucords-installer/issues/15) - Fedora check fails on RHEL8
- [Issue 36](https://github.com/quipucords/quipucords-installer/issues/36) - Installer attempted to install docker twice from local rpm
- [Issue 102](https://github.com/quipucords/quipucords-installer/pull/102) - Fix epel check with ansible yum module
- [Issue 105](https://github.com/quipucords/quipucords-installer/issues/105) - Support Podman to Podman upgrade
- [Issue 23](https://github.com/quipucords/quipucords-installer/issues/23) - Resolve the warning when checking for epel release
- [Issue 14](https://github.com/quipucords/qpc-tools/issues/14) - Replace QPC in the task names to something downstream friendly
- [Issue 17](https://github.com/quipucords/qpc-tools/issues/17) - Can not use relative paths in volume mappings with podman
- [Issue 51](https://github.com/quipucords/qpc-tools/issues/51) - Change the args/prompts dictionary to be an Ordered dictionary
- [Issue 40](https://github.com/quipucords/quipucords-installer/issues/40) - Remove checking for local cli rpm if installing with internet connectivity
- [Issue 43](https://github.com/quipucords/quipucords-installer/issues/43) - Offline install still tries to install dependencies for RHEL7 resulting in traceback


