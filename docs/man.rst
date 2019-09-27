qpc-tools
=========

Name
----

qpc-tools - Configuration tools for the Quipucords server and command line interface client.


Synopsis
--------

``qpc-tools command [options]``

Description
-----------

The ``qpc-tools`` package is used to configure the Quipucords server and command line interface (CLI) client.

Usage
-----

To install the Quipucords server and command line interfaced (CLI) client:

  ``qpc-tools install [options]``

The following sections describe these commands, their subcommands, and their options in more detail. They also describe additional tasks that are not highlighted in the previous list of major workflow tasks.

Installation
------------
The ``qpc-tools install`` command with no options performs a basic installation with the preset defaults. However, it is recommended the ``qpc-tools install`` command with options to change default username and passwords. The most common scenarios where you might use options to change the basic installation process are explained in the `Installing offline`_, `Installing a specific version`_, and `Installing the server and command line interface separately`_ sections.

Note that in log information for the ``qpc-tools install`` command, references to ``quipucords server`` are relevant to the Quipucords server, and references to ``qpc CLI`` are relevant to the Quipucords command line interface client.

  ``qpc-tools install [options]``

Options
~~~~~~~

The ``extra-vars`` options set values that are passed to the Ansible playbook that runs during installation.

**qpc-tools install (-e | --extra-vars) option=** *value*

The following list contains the available ``--extra-vars`` options.

``-e install_server=false``

  Controls the installation of the Quipucords server. Contains a true or false value. Defaults to ``true``. Supply ``false`` to skip the installation of the server.

``-e install_cli=false``

  Controls the installation of the Quipucords CLI. Contains a true or false value. Defaults to ``true``. Supply ``false`` to skip the installation of the CLI.

``-e install_offline=true``

  Controls whether the installation runs as an online (connected) installation or an offline (disconnected) installation. Contains a true or false value. Defaults to ``false``. Supply ``true`` to start an offline installation.

``-e server_version=0.9.0``

  Enables the installation of a specific Quipucords server version. Contains the semantic versioning format (version.release.patch, such as 0.9.0) of the Quipucords server that you want to install. Required if ``install_offline=true`` and ``install_server=true``.

``-e cli_version=0.9.0``

  Enables the installation of a specific Quipucords CLI version. Contains the semantic versioning format (version.release.patch, such as 0.9.0) of the Quipucords CLI that you want to install. Required if ``install_offline=true`` and ``install_cli=true``.

``-e server_port=8443``

  Sets the port number for the Quipucords server. Defaults to ``9443``.

``-e open_port=false``

  Determines whether to open the ``server_port`` in the firewall during the installation. This option enables communication between the Quipucords server and any remote clients over the port defined in ``server_port``. Contains a true or false value. Defaults to ``true``. Supply ``false`` to install without opening the server port in the firewall. The installation script must run with elevated privileges to open the server port.

``-e  dbms_user=postgres``

  Specifies the database user for PostgreSQL. Defaults to ``postgres``.

``-e dbms_password=pass123``

  Specifies the database password for PostgreSQL. Defaults to ``password``.

``-e server_username=adminid1``

  Sets the Quipucords server user name. Defaults to ``admin``.

``-e server_password=adminpw1``

  Sets the Quipucords server password. Defaults to ``qpcpassw0rd``.

``-e server_user_email=adminid1@example.com``

  Sets the Quipucords server user email address. Defaults to ``admin@example.com``.

``-e use_supervisord=false``

  Controls whether to start the Quipucords server with supervisord. Contains a true or false value. Defaults to ``true``. Supply ``false`` to start the server without supervisord.

``-e quipucords_home=~/quipucords_home``

  Sets the fully qualified path to the installation directory for the Quipucords server. Defaults to ``~/quipucords/``.

``-e offline_files=~/offline``

  Sets the fully qualified path to the files needed to complete an offline installation. Required if ``install_offline=true``.

``-e server_name=quipucords2``

  Sets the name for the Quipucords server. Defaults to ``quipucords``.

``-e server_http_timeout=90``

  Sets the HTTP timeout length for the Quipucords server. Defaults to ``120``.

``-e inspect_job_timeout=10700``

  Sets the network inspection scan timeout in seconds. Defaults to ``10800`` (3 hours).

``-e connect_job_timeout=500``

  Sets the network connection scan timeout in seconds. Defaults to ``600`` (10 minutes).

``-e ansible_log_level=10``

  Sets the level of log output by Ansible during network scans. Defaults to ``0``, which is the value for no extended logs.

Installing offline
------------------
If you choose the offline option to run the install command, you must do the following steps:

#. Obtain the installation packages on a machine with internet connectivity.

#. Create a location for the packages on the machine where Quipucords will be installed and move the packages to that location.

#. Run the qpc-tools with the required options to complete an offline installation.

Obtaining packages
~~~~~~~~~~~~~~~~~~
Download the following packages to the machine with internet connectivity. Make sure that the package names match the default names in the following instructions.

*Quipucords server*

#. Go to the following URL: https://github.com/quipucords/quipucords/releases

#. Download the ``quipucords_server_image.tar.gz`` package.

*PostgreSQL*

#. Create the PostgreSQL image TAR file with Docker. Use the the following command, where the package name is ``postgres.9.6.10.tar``:

   ``docker pull postgres:9.6.10 && docker save -o postgres.9.6.10.tar postgres:9.6.10``

*qpc tools command line interface*

#. Go to the following URL: https://github.com/quipucords/qpc/releases

#. Download the package that is applicable to the operating system version:
   - Red Hat Enterprise Linux 6 and CentOS 6: ``qpc.el6.noarch.rpm``
   - Red Hat Enterprise Linux 7 and CentOS 7: ``qpc.el7.noarch.rpm``

Setting the package location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Create a packages directory the following paths. For the variable marked as ``{lib}``, enter the library version, either lib or lib64. For the variable marked as ``{x.y.z}``, enter the version of the qpc-tools:

   ``mkdir -p /usr/{lib}/qpc-tools-{x.y.z}/install/packages``

#. Move the packages to the following directory so that the install command can find them:

   ``mv path/to/quipucords_server_image.tar.gz /usr/{lib}/qpc-tools-{x.y.z}/install/packages``

Running the offline installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To complete an installation on a machine without internet connectivity, also known as an offline installation, run the ``qpc-tools`` command with the appropriate options. For example, if you are installing version 0.9.0 of the Quipucords server and command line interface, you would enter the following command:

``qpc-tools install -e install_offline=true -e server_version=0.9.0  -e cli_version=0.9.0``

Installing a specific version
-----------------------------
By default, the ``qpc-tools`` command installs the latest release unless an earlier version is specified in the command. For example, if the previous version of Quipucords that you want to install is 0.9.0., you would enter the following command:

``qpc-tools install -e server_version=0.9.0  -e cli_version=0.9.0``

Installing the server and command line interface separately
-----------------------------------------------------------
The default installation process installs the Quipucords server and command line interface at the same time. However, you can choose to install the server and command line interface on seperate machines, as described in the following sections.

Installing the server without the command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example command installs the Quipucords server but does not install the command line interface.

``qpc-tools install -e install_cli=false``

Installing the command line interface without the server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example command installs the Quipucords command line interface but does not install the server.

``qpc-tools install -e install_server=false``

Options for All Commands
------------------------

The following options are available for every Quipucords command.

``--help``

  Prints the help for the ``qpc-tools`` command.

Authors
-------

The qpc-tools was originally written by Chris Hambridge <chambrid@redhat.com>, Kevan Holdaway <kholdawa@redhat.com>, Ashley Aiken <aaiken@redhat.com>, Cody Myers <cmyers@redhat.com>, and Dostonbek Toirov <dtoirov@redhat.com>.

Copyright
---------

Copyright 2019 Red Hat, Inc. Licensed under the GNU Public License version 3.
