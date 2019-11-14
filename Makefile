test:
	pytest -s  tests/*.py
install:
	pip3 uninstall bell -y
	pip3 install . --user
