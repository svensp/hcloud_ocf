all: requirements dist/floating_ip dist/alias_ip dist/hetzner_cloud 

requirements: requirements.txt
	pip3 install -r requirements.txt

dist/floating_ip: floating_ip.py
	pyinstaller -F floating_ip.py

dist/alias_ip: alias_ip.py
	pyinstaller -F alias_ip.py

dist/hetzner_cloud: hetzner_cloud.py
	pyinstaller -F hetzner_cloud.py

test:
	nosetests tests/*

clean:
	rm -Rf __pycache__ **/__pycache__ build dist
	find -type d -name __pycache__ | xargs rm -Rf
