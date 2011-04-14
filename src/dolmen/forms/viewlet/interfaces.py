# -*- coding: utf-8 -*-

from dolmen.forms.base.interfaces import IFormCanvas


class IInlineForm(IFormCanvas):
    """A form that can be inserted inside an another page / layout.
    """
