# Hetzner Cloud STONITH agent
This stonith agent uses the hetzner cloud api to fence(reboot) machines which
become unresponsive

## Installation
The stonith agent is written for python3 so you will have to install it on your
system. The packages executables available in the releases try to include their
extensions. The following extensions need to be present on the system however
because they do not work from inside the packaged executable:

- lxml
- hetznercloud

To install them use:

	sudo pip3 install hetznercloud lxml

Now download the `hetzner_cloud` executable from the releases page and move it to
the pacemaker stonith agent directory `/usr/lib/stonith/plugins/external/`.

## Use
Example

	pcs resource create stonith_hostX stonith:external/hetzner_cloud api_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 
	pcs constraint location stonith_hostX avoids hostX

### Options
#### Required
- `api_token` the hetzner cloud api token required to access the project
#### Optional
- `sleep`: Time to sleep before retrying when an api request fails. Defaults to
  5 seconds
- `hostname_to_api`: This option can be used to translate between hostnames as
  pacemaker sees the and hostnames in the cloud api if they don't match for
  whatever reason. Format: `hostname:apiname[,hostname2:apiname2,...]`
- `fail_on_host_find_failure`: If this option is set to true then not finding the
  host when looking for it in the cloud api will exit the action with a failure.
  It feels logically that this should be done but in the past hosts have not
  been present in the answers of the api for no discernable reason and simply
  retrying the request solved this problem.
