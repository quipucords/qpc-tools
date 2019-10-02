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

``--offline_files=OFFLINE_FILES``

  Sets the fully qualified path to the files needed to complete an offline installation. Required if ``offline`` specified.

``--version=VERSION``

  Enables the installation of a specific Quipucords server version. Contains the semantic versioning format (version.release.patch, such as 0.9.0) of the Quipucords server that you want to install. Required if ``install_offline=true`` and ``install_server=true``.

``--home_dir=HOME_DIR``

  Sets the fully qualified path to the installation directory for the Quipucords server. Defaults to ``~/quipucords/``.

``--server_port=SERVER_PORT``

  Sets the port number for the Quipucords server. Defaults to ``9443``.

``--open_port=OPEN_PORT``

  Determines whether to open the ``server_port`` in the firewall during the installation. This option enables communication between the Quipucords server and any remote clients over the port defined in ``server_port``. Contains a true or false value. Defaults to ``true``. Supply ``false`` to install without opening the server port in the firewall. The installation script must run with elevated privileges to open the server port.

``--dbms_user=DBMS_USER``

  Specifies the database user for PostgreSQL. Defaults to ``postgres``.

``--dbms_password=DBMS_PASSWORD``

  Specifies the database password for PostgreSQL. Defaults to ``password``.

``--server_username=SERVER_USERNAME``

  Sets the Quipucords server user name. Defaults to ``admin``.

``--server_password=SERVER_PASSWORD``

  Sets the Quipucords server password. Defaults to ``qpcpassw0rd``.


Installing the server offline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you choose the offline option to run the install command, you must do the following steps:

#. Obtain the installation packages on a machine with internet connectivity.

#. Create a location for the packages on the machine where Quipucords will be installed and move the packages to that location.

#. Run the qpc-tools with the required options to complete an offline installation.  For example::

    qpc-tools server install --offline --offline-files='/PATH' --version=0.9.1


Obtaining the server packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download the following packages to the machine with internet connectivity. Make sure that the package names match the default names in the following instructions.

*Quipucords server*

#. Go to the following URL: https://github.com/quipucords/quipucords/releases

#. Download the ``quipucords_server_image.tar.gz`` package.

*PostgreSQL*

#. Create the PostgreSQL image TAR file with Docker. Use the the following command, where the package name is ``postgres.9.6.10.tar``::

    docker pull postgres:9.6.10 && docker save -o postgres.9.6.10.tar postgres:9.6.10


Setting the package location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Create a packages directory the following paths. For the variable marked as ``{lib}``, enter the library version, either lib or lib64. For the variable marked as ``{x.y.z}``, enter the version of the qpc-tools::

    mkdir -p /usr/{lib}/qpc-tools-{x.y.z}/install/packages

#. Move the packages to the following directory so that the install command can find them::

    mv path/to/quipucords_server_image.tar.gz /usr/{lib}/qpc-tools-{x.y.z}/install/packages

Running the offline installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To complete an installation on a machine without internet connectivity, also known as an offline installation, run the ``qpc-tools server install`` command with the appropriate options. For example, if you are installing version 0.9.1 of the Quipucords server and command line interface, you would enter the following command::

    qpc-tools server install --offline --offline-files='/PATH' --version=0.9.1

Installing a specific version of the server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, the ``qpc-tools server install`` command installs the latest release unless an earlier version is specified in the command. For example, if the previous version of Quipucords that you want to install is 0.9.0., you would enter the following command::

    qpc-tools server install --version=0.9.0

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