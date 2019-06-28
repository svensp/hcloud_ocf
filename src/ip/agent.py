from ocf.resource_agent import ResourceAgent

class FloatingIp(ResourceAgent):
    def __init__(self):
        super().__init__()
        self.meta.setDescription(
                'Control a hetzner cloud floating ip address',
                '''This agent uses the hetzner cloud api to direct a cloud
                floating ip address to the server the resource is started on.

                Monitor will report running on the server the floating ip is
                pointing to.

                Stop currently does nothing as it is not strictly necessary to
                clear the ip address target before reassigning it and actually
                doing so has caused issues in the past.

                Please note that for the server to accept packets on the ip it
                is also necessary to add the ip address to the hosts network
                interface.
                This can be done permanently by adding `ip addr add ...` to the
                servers network configuration.
                Or you can use the IPAddr2 agent to build a resource which
                follows the floating ip

                Note that permanently adding the ip address to a node has the
                disadvantage that packets from the host sent to the given ip
                will always be sent to loopback and not leave the server, regardless
                whether or not the server currently has the ip address.
                ''')

    def start(self):
        self.retrieveServer()

        self.retrieveIp()

        self.assignIpToServer()

    def monitor(self):
        pass

    def retrieveServer(self):
        self.server = self.server.retrieve()

    def retrieveIp(self):
        self.ip = self.ip.retrieve()

    def assignIpToServer(self):
        self.ip.setTargetServer(self.server).assign()
