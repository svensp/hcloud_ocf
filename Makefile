all: floating_ip hetzner_cloud

floating_ip:

hetzner_cloud:

clean:
	rm -Rf build dist **/__pycache__

test: 
	nosetests3
