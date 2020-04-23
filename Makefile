test:
	pytest -s  tests/*.py
sync:
	rsync -av  --exclude-from=/home/garfield/bin/projects-excluded ./ firefly:python/
sync-prod:
	rsync -av  --exclude-from=/home/garfield/bin/projects-excluded ./  firefly-prod:python/
install:
	pip3 uninstall bell -y
	pip3 install . --user
build-remote: sync
	ansible-playbook bell.python.ansible.yml
