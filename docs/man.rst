qpc-tools
=========

Name
----

qpc-tools - Configuration tools for the Quipucords server and command line interface client.


Synopsis
--------

``qpc-tools command subcommand [options]``

Description
-----------

The ``qpc-tools`` package is used to configure the Quipucords server and command line interface (CLI) client.

Usage
-----

To install the Quipucords server and command line interfaced (CLI) client:

  ``qpc-tools install [options]``

The following sections describe these commands, their subcommands, and their options in more detail. They also describe additional tasks that are not highlighted in the previous list of major workflow tasks.

Server
------

Server Installation
^^^^^^^^^^^^^^^^^^^
The ``qpc-tools server install`` command with no options performs a basic installation with the preset defaults. However, it is recommended the ``qpc-tools server install`` command with options to change default username and passwords. The most common scenarios where you might use options to change the basic installation process are explained in the `Installing the server offline`_ and  `Installing a specific version of the server`_ sections.

Note that in log information for the ``qpc-tools server install`` command, references to ``quipucords server`` are relevant to the Quipucords server, and references to ``qpc CLI`` are relevant to the Quipucords command line interface client.

**qpc-tools server install** [**-h**]
                         [**--offline**]
                         [**--offline-files** *OFFLINE_FILES*]
                         [**--version** *SERVER_VERSION*]
                         [**--home-dir** *HOME_DIR*]
                         [**--port** *SERVER_PORT*]
                         [**--open-port** *OPEN_PORT*]
                         [**--dbms-user** *DBMS_USER*]
                         [**--dbms-password** *DBMS_PASSWORD*]
                         [**--username** *SERVER_USERNAME*]
                         [**--password** *SERVER_PASSWORD*]

``--offline``

  Controls whether the installation runs as an offlien (disconnected) installation.

``--offline-files=OFFLINE_FILES``

  Sets the fully qualified path to the files needed to complete an offline installation. Required if ``offline`` specified.

``--version=VERSION``

  Enables the installation of a specific Quipucords server version. Contains the semantic versioning format (version.release.patch, such as 0.9.0) of the Quipucords server that you want to install. Required if ``offline`` is specified.

``--home-dir=HOME_DIR``

  Sets the fully qualified path to the installation directory for the Quipucords server. Defaults to ``~/quipucords/``.

``--port=SERVER_PORT``

  Sets the port number for the Quipucords server. Defaults to ``9443``.

``--open-port=OPEN_PORT``

  Determines whether to open the ``port`` in the firewall during the installation. This option enables communication between the Quipucords server and any remote clients over the port defined in ``port``. Contains a true or false value. Defaults to ``true``. Supply ``false`` to install without opening the server port in the firewall. The installation script must run with elevated privileges to open the server port.

``--dbms-user=DBMS_USER``

  Specifies the database user for PostgreSQL. Defaults to ``postgres``.

``--dbms-password=DBMS_PASSWORD``

  Specifies the database password for PostgreSQL. Defaults to ``password``.

``--username=SERVER_USERNAME``

  Sets the Quipucords server user name. Defaults to ``admin``.

``--password=SERVER_PASSWORD``

  Sets the Quipucords server password. Defaults to ``qpcpassw0rd``.


Installing the server offline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you choose the offline option to run the install command, you must do the following steps:

#. Obtain the installation packages on a machine with internet connectivity.
  - Go to the following URL: https://github.com/quipucords/quipucords/releases
  - Download the ``quipucords_server_image.tar.gz`` package.
  - Create the PostgreSQL image TAR file with Docker. Use the the following command, where the package name is ``postgres.9.6.10.tar``::

      docker pull postgres:9.6.10 && docker save -o postgres.9.6.10.tar postgres:9.6.10
#. Create a location for the packages on the machine where Quipucords will be installed and move the packages to that location.
#. Run the qpc-tools with the required options to complete an offline installation.  For example::

    qpc-tools server install --offline --offline-files='/PATH_TO_OFFLINE_FILES' --version=0.9.1


Installing a specific version of the server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, the ``qpc-tools server install`` command installs the latest release unless an earlier version is specified in the command. For example, if the previous version of Quipucords that you want to install is 0.9.0., you would enter the following command::

    qpc-tools server install --version=0.9.0

Command Line Interface (CLI)
----------------------------

CLI Installation
^^^^^^^^^^^^^^^^
The ``qpc-tools cli install`` command with no options performs a basic installation with the preset defaults.

Note that in log information for the ``qpc-tools cli install`` command, references to ``quipucords server`` are relevant to the Quipucords server, and references to ``qpc CLI`` are relevant to the Quipucords command line interface client.

**qpc-tools cli install** [**-h**]
                         [**--offline**]
                         [**--offline-files** *OFFLINE_FILES*]
                         [**--version** *SERVER_VERSION*]
                         [**--home-dir** *HOME_DIR*]
                         [**--server-host** *SERVER_HOST*]
                         [**--server-port** *SERVER_PORT*]

``--offline``

  Controls whether the installation runs as an offlien (disconnected) installation.

``--offline-files=OFFLINE_FILES``

  Sets the fully qualified path to the files needed to complete an offline installation. Required if ``offline`` specified.

``--version=VERSION``

  Enables the installation of a specific Quipucords CLI version. Contains the semantic versioning format (version.release.patch, such as 0.9.0) of the Quipucords CLI that you want to install.

``--home-dir=HOME_DIR``

  Sets the fully qualified path to the installation directory for the Quipucords CLI. Defaults to ``~/quipucords/``.

``--server-host=SERVER_HOST``

  Sets the host for the Quipucords server. Defaults to ``127.0.0.1``.

``--server-port=SERVER_PORT``

  Sets the port number for the Quipucords server. Defaults to ``9443``.


Installing the CLI offline
^^^^^^^^^^^^^^^^^^^^^^^^^^
If you choose the offline option to run the install command, you must do the following steps:

#. Obtain the installation packages on a machine with internet connectivity.
  - Go to the following URL: https://github.com/quipucords/qpc/releases
  - Download the package that is applicable to the operating system version:
    - Red Hat Enterprise Linux 6 and CentOS 6: ``qpc.el6.noarch.rpm``
    - Red Hat Enterprise Linux 7 and CentOS 7: ``qpc.el7.noarch.rpm``
    - Red Hat Enterprise Linux 8: ``qpc.el8.noarch.rpm``
#. Create a location for the packages on the machine where Quipucords will be installed and move the packages to that location.
#. Run the qpc-tools with the required options to complete an offline installation.  For example::

    qpc-tools cli install --offline --offline-files='/PATH_TO_OFFLINE_FILES'


Installing a specific version of the CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, the ``qpc-tools cli install`` command installs the latest release unless an earlier version is specified in the command. For example, if the previous version of Quipucords that you want to install is 0.9.0., you would enter the following command::

    qpc-tools cli install --version=0.9.0


Options for All Commands
^^^^^^^^^^^^^^^^^^^^^^^^

The following options are available for every Quipucords command.

``--help``

  Prints the help for the ``qpc-tools`` command.

Authors
-------

The qpc-tools was originally written by Chris Hambridge <chambrid@redhat.com>, Kevan Holdaway <kholdawa@redhat.com>, Ashley Aiken <aaiken@redhat.com>, Cody Myers <cmyers@redhat.com>, and Dostonbek Toirov <dtoirov@redhat.com>.

Copyright
---------

Copyright 2019 Red Hat, Inc. Licensed under the GNU Public License version 3.




















OFFLINE CLI STUFF

*qpc tools command line interface*

#. Go to the following URL: https://github.com/quipucords/qpc/releases

#. Download the package that is applicable to the operating system version:
   - Red Hat Enterprise Linux 6 and CentOS 6: ``qpc.el6.noarch.rpm``
   - Red Hat Enterprise Linux 7 and CentOS 7: ``qpc.el7.noarch.rpm``