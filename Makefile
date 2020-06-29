all: floating_ip alias_ip hetzner_cloud

floating_ip:
	pyinstaller floating_ip.py

alias_ip:
	pyinstaller alias_ip.py

hetzner_cloud:
	pyinstaller hetzner_cloud.py

test:
	nosetests tests/*

clean:
	rm -Rf __pycache__ **/__pycache__ build dist
	find -type d -name __pycache__ | xargs rm -Rf
