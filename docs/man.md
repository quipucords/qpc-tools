# qpc-tools

## Name

qpc-tools - Configuration tools for the Quipucords server and command line interface client.


## Synopsis

`qpc-tools command subcommand [options]`

## Description

The `qpc-tools` package is used to install and configure the Quipucords server and command line interface (CLI) client.

# Usage

The following sections describe these commands, their subcommands, and their options in more detail. They also describe additional tasks that are not highlighted in the previous list of major workflow tasks.

## Server

This section describes various `qpc-tools` commands for installing and configuring the Quipucords server.

### Server Install Command

Use the `qpc-tools server install` command to install and configure the Quipucords server. When running the `qpc-tools server install` command, the user can optionally specify both the server admin password and the database password. If either password is not specified, they will be prompted to enter it. Additionally, it is recommended to run the command with options to change default usernames.

**qpc-tools server install** [**-h**]
                         [**\--offline-files** *OFFLINE_FILES*]
                         [**\--version** *SERVER_VERSION*]
                         [**\--home-dir** *HOME_DIR*]
                         [**\--port** *SERVER_PORT*]
                         [**\--open-port** *OPEN_PORT*]
                         [**\--db-user** *DB_USER*]
                         [**\--db-password** *DB_PASSWORD*]
                         [**\--username** *SERVER_USERNAME*]
                         [**\--password** *SERVER_PASSWORD*]

`--offline-files=OFFLINE_FILES`

  Sets the fully qualified path to the files needed to complete an offline installation.

`--version=VERSION`

  Enables the installation of a specific Quipucords server version. Contains the semantic versioning format (version.release.patch, such as 0.9.1) of the Quipucords server that you want to install. Required if `offline-files` is specified.

`--home-dir=HOME_DIR`

  Sets the fully qualified path to the installation directory for the Quipucords server. Defaults to `~/quipucords/`.

`--port=SERVER_PORT`

  Sets the port number for the Quipucords server. Defaults to `9443`.

`--open-port=OPEN_PORT`

  Determines whether to open the `port` in the firewall during the installation. This option enables communication between the Quipucords server and any remote clients over the port defined in `port`. Contains a true or false value. Defaults to `true`. Supply `false` to install without opening the server port in the firewall. The installation script must run with elevated privileges to open the server port.

`--db-user=DB_USER`

  Specifies the database user for PostgreSQL. Defaults to `postgres`.

`--db-password=DB_PASSWORD`

  Specifies the database password for PostgreSQL.  If omitted, qpc-tools will prompt for the database password.  Note for upgrade installations you must provide the same password as the initial install.  If you installed using a Quipucords installer prior to qpc-tools 0.2.0, the default password was `password`.

`--username=SERVER_USERNAME`

  Sets the Quipucords server user name. Defaults to `admin`.

`--password=SERVER_PASSSWORD`

  Sets the Quipucords server password. If omitted, qpc-tools will prompt for Quipucords server password.


#### Installing the server offline

Install all dependencies for the target operating system. Dependencies include:

- **CentOS 6 and RHEL 6**
  - [Docker 1.7.1](http://yum.dockerproject.org/repo/main/centos/6/Packages/docker-engine-1.7.1-1.el6.x86_64.rpm)

- **CentOS 7, RHEL 7, and RHEL 8**
  - podman

Next complete the following steps.

1. Obtain the installation packages on a machine with internet connectivity.

    - Download the [Quipucords server image](https://github.com/quipucords/quipucords/releases/latest/download/quipucords_server_image.tar.gz)

    - Create the PostgreSQL image TAR file named `postgres.14.1.tar`

      - CentOS 6 and RHEL 6 commands:
        ```
        docker pull postgres:14.1
        docker save -o postgres.14.1.tar postgres:14.1
        ```

      - CentOS 7, RHEL 7, and RHEL 8 commands:
        ```
        podman pull postgres:14.1
        podman save -o postgres.14.1.tar postgres:14.1
        ```

1. Create a location for the packages on the machine where Quipucords will be installed and move the packages to that location.

1. Run qpc-tools with the required options to complete an offline installation. For example:

    ```
    qpc-tools server install --offline-files='/PATH' --version=0.9.1
    ```

#### Installing a specific version of the server

By default, the `qpc-tools server install` command installs the latest release unless an earlier version is specified in the command. For example, if the previous version of Quipucords that you want to install is 0.9.1, you would enter the following command:

```
qpc-tools server install --version=0.9.1
```

## Command Line Interface (CLI)

This section describes various `qpc-tools` commands for installing and configuring the Quipucrods CLI.

### CLI Install Command

The `qpc-tools cli install` command with no options performs a basic installation with the preset defaults.

Note that in the log information for the `qpc-tools cli install` command, references to `Quipucords server` are relevant to the Quipucords server, and references to `QPC CLI` are relevant to the Quipucords command line interface client.

**qpc-tools cli install** [**-h**]
                         [**\--offline-files** *OFFLINE_FILES*]
                         [**\--version** *CLI_VERSION*]
                         [**\--home-dir** *HOME_DIR*]
                         [**\--server-host** *SERVER_HOST*]
                         [**\--server-port** *SERVER_PORT*]

`--offline-files=OFFLINE_FILES`

  Sets the fully qualified path to the files needed to complete an offline installation.

`--version=VERSION`

  Enables the installation of a specific Quipucords CLI version. Contains the semantic versioning format (version.release.patch, such as 0.9.1) of the Quipucords CLI that you want to install.

`--home-dir=HOME_DIR`

  Sets the fully qualified path to the installation directory for the Quipucords CLI. Defaults to `~/quipucords/`.

`--server-host=SERVER_HOST`

  Sets the host for the Quipucords server. Defaults to `127.0.0.1`.

`--server-port=SERVER_PORT`

  Sets the port number for the Quipucords server. Defaults to `9443`.


#### Installing the CLI offline

Install all dependencies for the target operating system. Dependencies include:

- **CentOS 6 and RHEL 6**
  - python34-requests

- **CentOS 7**
  - epel-release
  - python36-requests

- **RHEL 7**
  - python36-requests

- **RHEL 8**
  - python3-requests

Next complete the following steps.

1. Obtain the installation packages on a machine with internet connectivity. Select the appropriate RPM for your operating system.

    - [Red Hat Enterprise Linux 6 and CentOS 6](https://github.com/quipucords/qpc/releases/latest/download/qpc.el6.noarch.rpm)

    - [Red Hat Enterprise Linux 7 and CentOS 7](https://github.com/quipucords/qpc/releases/latest/download/qpc.el7.noarch.rpm)

    - [Red Hat Enterprise Linux 8](https://github.com/quipucords/qpc/releases/latest/download/qpc.el8.noarch.rpm)

1. Create a location for the packages on the machine where Quipucords will be installed and move the packages to that location.

1. Run qpc-tools with the required options to complete an offline installation. For example:

    ```
    qpc-tools cli install --offline-files='/PATH'
    ```

#### Installing a specific version of the CLI
By default, the `qpc-tools cli install` command installs the latest release unless an earlier version is specified in the command. For example, if the previous version of Quipucords that you want to install is 0.9.1., you would enter the following command:

```
qpc-tools cli install --version=0.9.1
```

## Options for All Commands

The following options are available for every Quipucords command.

``--help``

  Prints the help for the ``qpc-tools`` command.

## Authors

The qpc-tools was originally written by [Chris Hambridge](mailto:chambrid@redhat.com), [Kevan Holdaway](mailto:kholdawa@redhat.com), [Ashley Aiken](mailto:aaiken@redhat.com), [Cody Myers](mailto:cmyers@redhat.com), and [Dostonbek Toirov](mailto:dtoirov@redhat.com).

## Copyright

Copyright 2019 Red Hat, Inc. Licensed under the GNU Public License version 3.