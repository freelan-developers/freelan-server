"""
The settings wizard view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template, abort
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, Setting

import M2Crypto as m2

@login_required
def settings_wizard(step=None):
    """
    The settings wizardview.
    """

    min_step=1
    max_step=3

    # Redirect if step is not defined
    if step is None:
        return redirect(url_for('settings_wizard', step=min_step))

    # Abort if step is invalid
    if (step < min_step) or (step > max_step):
        abort(404)

    authority_private_key = Setting.get_value('authority_private_key')

    return render_template(
        'pages/settings_wizard_%s.html' % step,
        step=step,
        min_step=min_step,
        max_step=max_step,
        authority_private_key=authority_private_key,
    )
