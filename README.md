# hcloud\_ocf
Hetzner Cloud Pacemaker OCF Resource Agents, FloatingIp and STONITH device

## Install
The following python extensions need to be present on your system:

- lxml
- hetznercloud

Download the zip-packaged distribution files from the releases page and place
them in your ocf resource agent directory and/or stonith plugin directory
- `floating_ip` is an ocf resource agent, the default directory for them ist `/usr/lib/ocf/resource.d/hetzner/`  
  Note that the hetzner directory may be named differently, but must match the resource agent name `ocf:DIRECTORY:floating_ip`
- `hetzner_cloud` is an ocf resource agent, the default directory for them ist `/usr/lib/stonith/plugins/external`

## Test
Copy .env.template to .env and add your hetzner cloud token and floating ip
address. Then source your .env before running the scripts

```sh
cp .env.template .env
. .env
python3 floating_ip start
```

Note that it is not strictly necessary to copy the .env.template file before
modifiying it. Doing so is to prevent accidently commiting it as the .env file
is in the .gitignore

## Usage
- [Floating IP Resource Agent](floating_ip)
- [Stonith device](stonith)

## Packages
### lxml
lxml uses c-code and thus cannot be loaded from a zip file

### hetznercloud
hetznercloud itself could be added to the package. The problem is in the
dependency to certifi. Certifi does not work from zip apps if they have a
shebang. My current guess on this is the fact that the cacert.pem is extracted
to a temporary location for openssl to use it but the extraction process fails
because of the shebang.
