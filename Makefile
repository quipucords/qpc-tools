DATE = $(shell date)
PYTHON = $(shell which python)
TOPDIR = $(shell pwd)
# Required for a work around in the spec file
pandoc = pandoc
.PHONY: install

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  setup-local-online                             Copy configuration, install, packages to OS specific folders"
	@echo "  setup-local-offline                            Download/Build qpc server and postgres images. Download qpc client rpm. Copy configuration, install, packages to OS specific folders"
	@echo "         server_source=<local||release>                @param - defaults to release"
	@echo "         cli_version=<x.x.x>                           @param - defaults to latest"
	@echo "         server_version=<x.x.x>                        @param - required if server source is local; defaults to latest if using release"
	@echo "  setup-release-online                           Download and copy qpc-tools to OS specific folders"
	@echo "         tools_version=<x.x.x>                         @param - defaults to latest"
	@echo "  setup-release-offline                          Download and copy qpc-tools, server image and qpc client rpm to OS specific folders"
	@echo "         tools_version=<x.x.x>                         @param - defaults to latest"
	@echo "         cli_version=<x.x.x>                           @param - defaults to latest"
	@echo "         server_version=<x.x.x>                        @param - defaults to latest"
	@echo "  refresh                                        Recopy configuration, install, packages to OS specific folders"
	@echo "  test-all                                       Launch VMs for all supported Operating Systems"
	@echo "  test-rhel-6                                    Launch the RHEL 6 VM for testing"
	@echo "  test-rhel-7                                    Launch the RHEL 7 VM for testing"
	@echo "  test-rhel-8                                    Launch the RHEL 8 VM for testing"
	@echo "  test-centos-6                                  Launch the CentOS 6 VM for testing"
	@echo "  test-centos-7                                  Launch the CentOS 7 VM for testing"
	@echo "  manpage                                        Create the manpage"
	@echo "  install                                        Install the client egg"
	@echo "  lint                                           Run the flake8/pylint linter"
	@echo "  unit-test                                      Run the python unit tests"
	@echo "  test-coverage                                  Run the unit tests and measure test coverage"
	@echo "  clean                                          Cleanup configure files and destroy VMs"

# Internal subcommands that the user should not call
create-test-dirs:
	mkdir -p test/packages
	@for os in rhel6 rhel7 rhel8 centos6 centos7; do \
		set -x; \
		mkdir -p test/$$os/install/; \
		mkdir -p test/$$os/config/rhel6; \
		mkdir -p test/$$os/config/rhel7; \
		mkdir -p test/$$os/scripts/; \
		set +x; \
	done

copy-vm-helper-files:
	for os in rhel6 rhel7 rhel8 centos6 centos7 ; do cp -vrf vm_helper_files/ test/$$os; done

# Internal subcommands that the user should not call
copy-config:
	@if [ -e tools_config.tar.gz ]; then \
		set -x; \
		mkdir -p test/helpers | true; \
		tar -xvf tools_config.tar.gz | true; \
		cp -rf tools_config/* test/helpers | true; \
		rm -rf tools_config/ | true; \
		for dest in test/rhel8 test/rhel7 test/rhel6 test/centos6 test/centos7 ; do cp -vrf test/helpers/* $$dest | true; done; \
		rm -rf test/helpers | true; \
		set +x; \
	else \
		echo "tools_config.tar.gz does not exist"; \
	fi

# Internal subcommands that the user should not call
copy-packages:
	for os in rhel6 rhel7 rhel8 centos6 centos7 ; do cp -vrf test/packages/ test/$$os/install/packages/ ; done

# Internal subcommands that the user should not call
copy-install: copy-qpc-tools
	for os in rhel6 rhel7 rhel8 centos6 centos7 ; do cp -vrf install test/$$os; done

copy-qpc-tools:
	for os in rhel6 rhel7 rhel8 centos6 centos7 ; do cp -vrf qpc_tools test/$$os; done
	for os in rhel6 rhel7 rhel8 centos6 centos7 ; do cp -vrf setup.py test/$$os; done
	for os in rhel6 rhel7 rhel8 centos6 centos7 ; do cp -vrf bin test/$$os; done


# Internal subcommands that the user should not call
local-server-image: download-postgres
	@echo "Building quipucords $(server_version)"
	cd ../quipucords;make build-ui
	cd ../quipucords;docker -D build . -t quipucords:$(server_version)
	cd ../quipucords;docker save -o quipucords_server_image.tar quipucords:$(server_version)
	cd ../quipucords;gzip -f quipucords_server_image.tar
	mv ../quipucords/quipucords_server_image.tar.gz test/packages/

# Internal subcommands that the user should not call
download-server-image: download-postgres
ifeq ($(server_version),$(filter $(server_version),latest))
	@echo "Downloading quipucords latest"
	cd test/packages; curl -k -SL https://github.com/quipucords/quipucords/releases/latest/download/quipucords_server_image.tar.gz -o quipucords_server_image.tar.gz
else
	@echo "Downloading quipucords $(server_version)"
	cd test/packages; curl -k -SL https://github.com/quipucords/quipucords/releases/download/$(server_version)/quipucords_server_image.tar.gz -o quipucords_server_image.tar.gz
endif

# Internal subcommands that the user should not call
download-client:
	@for os_version in 6 7 8 ; do \
		set -x; \
		if [[ "$(cli_version)" = "" || "$(cli_version)" = "latest" ]]; then \
			curl -k -SL https://github.com/quipucords/qpc/releases/latest/download/qpc.el$$os_version.noarch.rpm -o test/packages/qpc.el$$os_version.noarch.rpm; \
		else \
			curl -k -SL https://github.com/quipucords/qpc/releases/download/$(cli_version)/qpc.el$$os_version.noarch.rpm -o test/packages/qpc.el$$os_version.noarch.rpm; \
		fi; \
		cp -f test/packages/qpc.el$$os_version.noarch.rpm test/rhel$$os_version/install/packages/; \
		cp -f test/packages/qpc.el$$os_version.noarch.rpm test/centos$$os_version/install/packages/; \
		set +x; \
	done
	rm -f test/packages/*.noarch.rpm

# Internal subcommands that the user should not call
download-tools:
	mkdir -p test/downloaded_install
ifeq ($(tools_version),$(filter $(tools_version),latest))
	cd test/downloaded_install;curl -k -SL https://github.com/quipucords/qpc-tools/releases/latest/download/quipucords_install.tar.gz -o quipucords_install.tar.gz
else
	cd test/downloaded_install;curl -k -SL https://github.com/quipucords/qpc-tools/releases/download/$(tools_version)/quipucords_install.tar.gz -o quipucords_install.tar.gz
endif
	cd test/downloaded_install;tar -xzf quipucords_install.tar.gz
	for os in rhel6 rhel7 rhel8 centos6 centos7 ; do cp -vrf test/downloaded_install/install test/$$os/; done
	rm -rf test/downloaded_install

# Internal subcommands that the user should not call
download-postgres:
	mkdir -p test/packages
	docker pull postgres:9.6.10
	cd test/packages;docker save -o postgres.9.6.10.tar postgres:9.6.10

setup-local-online: create-test-dirs copy-install copy-vm-helper-files copy-config

setup-local-offline: create-test-dirs copy-install copy-vm-helper-files copy-config
ifeq ($(server_source),local)
ifeq ($(server_version),)
	@echo "Server version is not provided. Exiting...";
	@exit 1;
else
	$(MAKE) local-server-image;
endif
else
ifeq ($(server_source),release)
	$(MAKE) download-server-image;
else
	@echo "Quipucords server source not defined.";
	@echo "Setting release as default server source.";
	$(MAKE) download-server-image;
endif
endif
	$(MAKE) copy-packages
	$(MAKE) download-client

setup-release-online: create-test-dirs copy-vm-helper-files copy-config copy-packages
	$(MAKE) download-tools

setup-release-offline: create-test-dirs copy-vm-helper-files copy-config copy-packages
	$(MAKE) download-tools
	$(MAKE) download-server-image
	$(MAKE) download-client
	$(MAKE) copy-packages

refresh: create-test-dirs copy-vm-helper-files copy-config copy-install copy-packages

test-all:
	./launch_vms.sh

test-rhel-6:
	vagrant up vrhel6;vagrant ssh vrhel6

test-rhel-7:
	vagrant up vrhel7;vagrant ssh vrhel7

test-rhel-8:
	vagrant up vrhel8;vagrant ssh vrhel8

test-centos-6:
	vagrant up vcentos6;vagrant ssh vcentos6

test-centos-7:
	vagrant up vcentos7;vagrant ssh vcentos7

clean-local-cli:
	rm -rf dist/ build/ qpc_tools.egg-info/

clean: clean-local-cli
	vagrant destroy -f
	rm -rf test

manpage:
	$(pandoc) docs/man.rst \
	  --standalone -t man -o docs/qpc-tools.1 \
	  --variable=section:1 \
	  --variable=date:'June 6, 2019' \
	  --variable=footer:'version 0.9.1' \
	  --variable=header:'qpc-tools'

# Install python egg
OMIT_PATTERNS = */test*.py,*/.virtualenvs/*.py,*/virtualenvs/*.py,.tox/*.py

install:
	$(PYTHON) setup.py build -f
	$(PYTHON) setup.py install -f

lint:
	tox -e lint

unit-test:
	tox -e py36

test-coverage:
	coverage run -m unittest discover qpc_tools/ -v
	coverage report -m --omit $(OMIT_PATTERNS)
	echo $(OMIT_PATTERNS)
