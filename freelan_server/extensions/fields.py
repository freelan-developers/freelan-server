"""
Specific fields.
"""

from wtforms import TextField

from freelan_server.extensions.widgets import IPTextInput

class IPTextField(TextField):
    """
    An IPv4 & IPv6 address text field.

    Can be used to input either a host address or a network address.
    """

    IP_VERSION_4 = 4
    IP_VERSION_6 = 6
    IP_VERSION_4_OR_6 = None

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
