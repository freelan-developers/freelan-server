"""
Specific widgets.
"""

from jinja2 import Markup
from wtforms.widgets import Select as wtfSelect
from wtforms.widgets import TextInput as wtfTextInput

class Select(wtfSelect):
    """
    Renders a select input.

    Pretty much the same as a wtforms.widgets.Select except that a custom
    labelizer method can be specified to customize the rendering of the labels.
    """

    def __init__(self, multiple=False, labelizer=None):
        super(Select, self).__init__(multiple=multiple)
        self.labelizer = labelizer

    def render_option(self, value, label, selected, **kwargs):
        if self.labelizer:
            label = self.labelizer(label)

        return wtfSelect.render_option(value, label, selected, **kwargs)

class IPTextInput(wtfTextInput):
    """
    Renders an IP select input.
    """

    def __call__(self, field, **kw):
        """
        Renders the widget.
        """

        ip_address_classes = ['ip-address-input']

        if field.ip_version:
            ip_address_classes.append('ipv%s-address-input' % field.ip_version)

        kw['class'] = ' '.join(kw.get('class', '').split() + ip_address_classes)

        return super(IPTextInput, self).__call__(field, **kw)
