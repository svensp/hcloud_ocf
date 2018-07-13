# hcloud_ocf
Hetzner Cloud Pacemaker OCF Resource Agents, FloatingIp and STONITH device

## Required modules
Might be packaged into the built zip file at some future point.

- hetznercloud
- ifaddr

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
