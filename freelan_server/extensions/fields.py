"""
Specific fields.
"""

from wtforms import TextField
from IPy import IP

from freelan_server.extensions.widgets import IPTextInput

class IPTextField(TextField):
    """
    An IPv4 & IPv6 address text field.

    Can be used to input either a host address or a network address.
    """

    IP_VERSION_4_OR_6 = 0
    IP_VERSION_4 = 4
    IP_VERSION_6 = 6

    def __init__(self,
                 label=None,
                 validators=None,
                 filters=(),
                 description=u'',
                 id=None,
                 default=None,
                 widget=None,
                 _form=None,
                 _name=None,
                 _prefix='',
                 _translations=None,
                 ip_version=IP_VERSION_4,
                 network_only=False
                ):
        """
        Create an IP text field.

        ip_version can be either IP_VERSION_4, IP_VERSION_6 or
        IP_VERSION_4_OR_6 (the default) to force input for an IPv4 address, an
        IPv6 address or both.

        network_only may be specified to force the input of a network address
        instead of a host address.
        """

        super(IPTextField, self).__init__(
            label=label,
            validators=validators,
            filters=filters,
            description=description,
            id=id,
            default=default,
            widget=widget or IPTextInput(),
            _form=_form,
            _name=_name,
            _prefix=_prefix,
            _translations=_translations,
        )

        self.ip_version = ip_version
        self.network_only = network_only

    def pre_validate(self, form):

        if self.data:
            try:
                self.data = str(self.ip_address)
            except Exception, ex:
                if self.network_only:
                    if self.ip_version == IPTextField.IP_VERSION_4:
                        raise ValueError('An IPv4 network address is expected. Example: 10.0.0.0/16, 192.168.0.0/24')
                    elif self.ip_version == IPTextField.IP_VERSION_6:
                        raise ValueError('An IPv6 network address is expected. Example: fe80::/64, fe80::ab00/8')
                    else:
                        raise ValueError('An IPv4 or IPv6 network address is expected. Example: 10.0.0.0/16, fe80::/64')
                else:
                    if self.ip_version == IPTextField.IP_VERSION_4:
                        raise ValueError('An IPv4 address is expected. Example: 10.0.0.1, 192.168.0.1')
                    elif self.ip_version == IPTextField.IP_VERSION_6:
                        raise ValueError('An IPv6 address is expected. Example: fe80::1, fe80::ab01')
                    else:
                        raise ValueError('An IPv4 or IPv6 address is expected. Example: 10.0.0.1, fe80::1')
        else:
            self.data = None

    def get_ip_address(self):
        """
        Get the associated IP address, if any or None otherwise.

        A ValueError is raised if the data is not a valid IP address.
        """

        if self.data:
            return IP(self.data, ipversion=self.ip_version, make_net=self.network_only)

    ip_address = property(get_ip_address)
