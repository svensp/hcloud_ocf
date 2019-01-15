# hcloud\_ocf
Pacemaker OCF Resource Agents to manage Hetzner Cloud resources.

## Floating Ip
Floating ips are also known as failover ips. They can be switched between hosts.

[Floating IP Resource Agent](floating_ip)

## Fencing / Stonith
Stonith devices ensure data safety by 'killing' a node believed to have failed.

This protects against the following scenario:
- Two hosts lose connection with eachother
- both allow edit to the data but can no longer sync it with the other host
- when they reconnect both have different 'current' data which cannot be merged
  back together automatically(or at all)

Think of it as both hosts creating a git branch of the data when they split,
except there is no merge functionality.

[Stonith device](stonith)

## Volume
Hetzner volumes provide attachable storage block devices on which filesystems
can be written and used like any other disk drive. They serve roughly the same
purpose as a drbd master/slave installation.

Not yet implemented.

### Development

#### Test
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

#### Packages
This section lists why packages cannot be packaged into the executable.

##### lxml
lxml uses c-code and thus cannot be loaded from a zip file

##### hetznercloud
hetznercloud itself could be added to the package. The problem is in the
dependency to certifi. Certifi does not work from zip apps if they have a
shebang. My current guess on this is the fact that the cacert.pem is extracted
to a temporary location for openssl to use it but the extraction process fails
because of the shebang.
