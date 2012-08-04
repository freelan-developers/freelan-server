"""
IP address management.
"""

from IPy import IP as ipyIP

class IP(ipyIP):
    """
    An IP address management class.
    """

    def isNetwork(self):
        """
        Check if the IP address is a network address.
        """

        return (self.len() > 1)

    def firstNetworkAddress(self):
        """
        Get the first address of the network address range.
        """

        if self.isNetwork():
            return IP(self.ip + 1)

    def lastNetworkAddress(self):
        """
        Get the last address of the network address range.
        """

        if self.isNetwork():
            return IP(self.ip + self.len() - 2)

    def networkAddresses(self):
        """
        Get the network addresses.
        """

        if self.isNetwork():
            ip = self.firstNetworkAddress()
            last_ip = self.lastNetworkAddress()

            yield ip

            while ip != last_ip:
                ip = IP(ip.ip + 1)
                yield ip
