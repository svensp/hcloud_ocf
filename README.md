# hcloud\_ocf
Hetzner Cloud Pacemaker OCF Resource Agents, FloatingIp and STONITH device

## Install

Download the zip-packaged distribution files from the releases page and place
them in your ocf resource agent directory and/or stonith plugin directory
- `FloatingIp` is an ocf resource agent, the default directory for them ist `/usr/lib/ocf/resource.d/hetzner/`  
  Note that the hetzner directory may be named differently, but must match the resource agent name `ocf:DIRECTORY:FloatingIp`
- `hetzner\_cloud` is an ocf resource agent, the default directory for them ist `/usr/lib/stonith/plugins/external`

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
