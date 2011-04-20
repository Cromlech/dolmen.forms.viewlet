====================
dolmen.forms.viewlet
====================

``dolmen.forms.viewlet`` provide you with a `Dolmen Form 
<http://pypi.python.org/pypi/dolmen.forms.base>`_ in a viewlet.

Example
=======

Quick example::

  from dolmen.forms import base
  from dolmen.forms.viewlet import ViewletForm

  class CallUs(ViewletForm):
     """A contact viewlet.
     """
     label = u"Call us"
     fields = base.Fields(base.Field("Phone number"))
     actions = base.Actions(base.Action("Call"))
