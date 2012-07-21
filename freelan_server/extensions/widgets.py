"""
Specific widgets.
"""

from jinja2 import Markup
from wtforms.widgets import Select as wtfSelect

class Select(wtfSelect):
    """
    Renders a select field.

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
