DATE = $(shell date)
TOPDIR = $(shell pwd)

.PHONY: install

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  setup                                              Sets up yum repos"
	@echo "  offline-prep                                       Install required dependencies for offline install"
	@echo "  online-prep                                        Install required dependencies for online install. Required if not using make commands."
	@echo "  clean                                              Remove docker containers and images.  Also, qpc cli."
	@echo "  install-local-tools                                Install the qpc-tools cli locally."

setup:
	scripts/setup_repos.sh

offline-prep: setup
	@if grep -q -i "release 7" /etc/redhat-release; then \
		echo "Running 7"; \
		yum install -y libcgroup; \
		yum install -y yum-utils; \
		yum install -y ansible; \
		yum install -y docker; \
		yum install -y podman; \
		yum install -y epel-release; \
		yum install -y python36; \
		yum install -y python36-requests; \
	elif grep -q -i "release 6" /etc/redhat-release; then \
		echo "Running 6"; \
		yum install -y libcgroup; \
		yum install -y yum-utils; \
		yum install -y ansible; \
		yum install -y xz; \
		cd install/packages/; curl -k -O -sSl http://yum.dockerproject.org/repo/main/centos/6/Packages/docker-engine-1.7.1-1.el6.x86_64.rpm; \
		rpm -Uvh --force "docker-engine-1.7.1-1.el6.x86_64.rpm"; \
		yum install -y python34; \
		yum install -y python34-requests; \
	else \
		echo "Running 8"; \
		yum install -y ansible; \
		yum install -y podman; \
		yum install -y python36; \
		yum install -y python3-requests; \
		yum install -y libselinux-python3; \
	fi

online-prep: setup
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

install-local-tools: online-prep
	sed -i "s?PLAYBOOK_PATH = ''?PLAYBOOK_PATH = '/qpc_tools/qpc_tools/install/ansible/'?g" qpc_tools/release.py
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