all: floating_ip hetzner_cloud

floating_ip:

hetzner_cloud:

requirements:
	pip3 install cerberus

clean:
	rm -Rf build dist **/__pycache__

test: 
	nosetests3
