all: venv_start

clean:
	find monu/ -name "*.pyc" -exec rm '{}' \;

clean_all:
	find monu/ -name ".DS_Store" -exec rm '{}' \;
	rm -rf build/ dist/ env/ *.egg-info

venv_start: venv_install
	sh contrib/venv/start.sh

venv_install: venv_install_data
	sh contrib/venv/install.sh

venv_install_data:
	sh contrib/venv/install_data.sh

docker_start: docker_build
	sh contrib/docker/start.sh

docker_install:
	sh contrib/docker/install_data.sh

docker_build: docker_install build

build:
	make -C menu-ui/Makefile

test:
	python -m unittest discover -s monu/test -p "*_test.py"

