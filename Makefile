all: requirements floating_ip alias_ip hetzner_cloud 

requirements: requirements.txt
	pip3 install -r requirements.txt

floating_ip:
	pyinstaller -F floating_ip.py

alias_ip:
	pyinstaller -F alias_ip.py

hetzner_cloud:
	pyinstaller -F hetzner_cloud.py

test:
	nosetests tests/*

clean:
	rm -Rf __pycache__ **/__pycache__ build dist
	find -type d -name __pycache__ | xargs rm -Rf
