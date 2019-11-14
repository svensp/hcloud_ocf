# Hetzner Cloud Floating IP resource agent
This resource agent controls a hetzner cloud floating ip address.

## Installation
### Automated
An automated install script exists but it is not yet extensivly tested.  
You still have to install python3 yourself with your distributions packaging
tool.

	curl 'https://gist.githubusercontent.com/svensp/1065ac4cbf9873a10eda7b85d4b5d07f/raw/a13680e97049d0d085e7794ac75e5e33b4cd8f85/install_hcloud_floating_ip.sh' | sudo sh

### Manual
The resource agent is written for python3 so you will have to install it on your
system. The packages executables available in the releases try to include their
extensions. The following extensions need to be present on the system however
because they do not work from inside the packaged executable:

- lxml
- hetznercloud

To install them use:

	sudo pip3 install hetznercloud lxml

Now download the `floating_ip` executable from the releases page and move it to
the pacemaker ocf agent directory `/usr/lib/ocf/resource.d/hetzner/`. Note that
the subdirectory `hetzner` will most likely have to be created.

## Examples
### Show the description of the resource agent and all available optoins

	pcs resource describe ocf:hetzner:floating_ip

### Create via pcs

	pcs resource create floating_ip ocf:hetzner:floating_ip ip=xxx.xxx.xxx.xxx api_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

### Create via crm
This example is a modified version of a command given in issue #1. I use pcs so
I do not have a way to test this command as of now. Please report success or
problems in Issue #2

	crm primitive vip_floating_ip ocf:hetzner:floating_ip \
		params ip=xxx.xxx.xxx.xxx api_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
		op start interval=0 timeout=20 \
		op stop interval=0 timeout=20 \
		op monitor interval=10 start-delay=0 timeout=20 
