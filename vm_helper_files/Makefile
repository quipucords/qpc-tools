DATE = $(shell date)
TOPDIR = $(shell pwd)

.PHONY: install

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  setup                                              Sets up yum repos"
	@echo "  offline-prep                                       Install required dependencies for offline install"
	@echo "  install-tools-deps                                 Install required dependencies for qpc-tools rpm."
	@echo "  clean                                              Remove docker containers and images.  Also, QPC cli."
	@echo "  install-local                                      Install the qpc-tools cli locally."
	@echo "  install-release-online                             Install the qpc-tools cli from online."
	@echo "         tools_version=<x.x.x>                         @param - defaults to latest"
	@echo "  install-release-offline                            Perform an offline installation of qpc-tools."


setup:
	scripts/setup_repos.sh

offline-prep: setup
	@if grep -q -i "release 7" /etc/redhat-release; then \
		echo "Running 7"; \
		yum install -y docker; \
		yum install -y podman; \
		yum install -y epel-release; \
		yum install -y python36-requests; \
	elif grep -q -i "release 6" /etc/redhat-release; then \
		echo "Running 6"; \
		yum install -y xz; \
		cd install/packages/; curl -k -O -sSl http://yum.dockerproject.org/repo/main/centos/6/Packages/docker-engine-1.7.1-1.el6.x86_64.rpm; \
		rpm -Uvh --force "docker-engine-1.7.1-1.el6.x86_64.rpm"; \
		yum install -y python34-requests; \
	else \
		echo "Running 8"; \
		yum install -y podman; \
		yum install -y python3-requests; \
		yum install -y libselinux-python3; \
	fi

install-tools-deps: setup
	@if grep -q -i "release 7" /etc/redhat-release; then \
		echo "Running 7"; \
		yum install -y libcgroup; \
		yum install -y yum-utils; \
		yum install -y ansible; \
		yum install -y python3; \
	elif grep -q -i "release 6" /etc/redhat-release; then \
		echo "Running 6"; \
		yum install -y libcgroup; \
		yum install -y yum-utils; \
		yum install -y ansible; \
		yum install -y python34; \
		yum install -y python34-setuptools; \
	else \
		echo "Running 8"; \
		yum install -y ansible; \
		yum install -y python36; \
	fi

clean:
	scripts/cleanup.sh

install-local: install-tools-deps
	python3 setup.py build
	@if grep -q -i "release 8" /etc/redhat-release; then \
	python3 setup.py install --prefix /usr; \
	else \
		python3 setup.py install; \
	fi
	echo ""
	echo "***************************"
	echo "WARNING: you will need to run the following for centos/rhel 7"
	echo "export PATH=$$PATH:/usr/local/bin" | xargs

install-release-online:
	@if [[ "$(tools_version)" = "" || "$(tools_version)" = "latest" ]]; then \
		if grep -q -i "release 7" /etc/redhat-release; then \
			yum install -y https://github.com/quipucords/qpc-tools/releases/latest/download/qpc-tools.el7.noarch.rpm; \
		elif grep -q -i "release 6" /etc/redhat-release; then \
			yum install -y https://github.com/quipucords/qpc-tools/releases/latest/download/qpc-tools.el6.noarch.rpm; \
		else \
			yum install -y https://github.com/quipucords/qpc-tools/releases/latest/download/qpc-tools.el8.noarch.rpm; \
		fi; \
	else \
		if grep -q -i "release 7" /etc/redhat-release; then \
			yum install -y https://github.com/quipucords/qpc-tools/releases/download/$(tools_version)/qpc-tools.el7.noarch.rpm; \
		elif grep -q -i "release 6" /etc/redhat-release; then \
			yum install -y https://github.com/quipucords/qpc-tools/releases/download/$(tools_version)/qpc-tools.el6.noarch.rpm; \
		else \
			yum install -y https://github.com/quipucords/qpc-tools/releases/download/$(tools_version)/qpc-tools.el8.noarch.rpm; \
		fi; \
	fi; \

install-release-offline: install-tools-deps
	@if grep -q -i "release 7" /etc/redhat-release; then \
		cd install; rpm -Uvh --force "qpc-tools.el7.noarch.rpm"; \
	elif grep -q -i "release 6" /etc/redhat-release; then \
		cd install; rpm -Uvh --force "qpc-tools.el6.noarch.rpm"; \
	else \
		cd install; rpm -Uvh --force "qpc-tools.el8.noarch.rpm"; \
	fi; \
