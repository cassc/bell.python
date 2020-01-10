test:
	pytest -s  tests/*.py
sync:
	rsync -av ./ fireprod-root:python/
	rsync -av --delete ./examples/ fireprod-root:/home/firefly/examples/
install:
	pip3 uninstall bell -y
	pip3 install .
build-remote: sync
	ansible-playbook bell.python.ansible.yml
