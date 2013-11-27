# -*- coding: utf-8 -*-

import os.path
import crom
from cromlech.browser import ITemplate
from dolmen.template import TALTemplate
from dolmen.viewlet import ViewletManager, Viewlet
from dolmen.forms.base import FormCanvas
from dolmen.forms.viewlet.interfaces import IInlineForm
from zope.interface import Interface, implementer


@implementer(IInlineForm)
class ViewletManagerForm(ViewletManager, FormCanvas):

    i18nLanguage = None

    def __init__(self, context, request, view):
        ViewletManager.__init__(self, context, request, view)
        FormCanvas.__init__(self, context, request)

    @property
    def prefix(self):
        return getattr(self.__class__, '__name__', None)

    @property
    def template(self):
        return ITemplate(self, self.request)

    def update(self):
        ViewletManager.update(self)
        FormCanvas.update(self)
        self.updateForm()

    def namespace(self):
        namespace = super(ViewletManagerForm, self).namespace()
        namespace['form'] = self
        if self.i18nLanguage is not None:
            namespace['target_language'] = self.i18nLanguage
        return namespace

    def updateForm(self):
        self.updateActions()
        self.updateWidgets()

    def render(self):
        return FormCanvas.render(self)


@implementer(IInlineForm)
class ViewletForm(Viewlet, FormCanvas):
    """A form as a viewlet.
    """
    i18nLanguage = None

    action_url = '.'

    def __init__(self, context, request, view, manager):
        Viewlet.__init__(self, context, request, view, manager)
        FormCanvas.__init__(self, context, request)

    @property
    def template(self):
        return ITemplate(self, self.request)

    def update(self):
        Viewlet.update(self)
        FormCanvas.update(self)
        self.updateForm()

    def namespace(self):
        namespace = super(ViewletForm, self).namespace()
        namespace['form'] = self
        if self.i18nLanguage is not None:
            namespace['target_language'] = self.i18nLanguage
        return namespace

    def updateForm(self):
        self.updateActions()
        self.updateWidgets()

    def render(self):
        return FormCanvas.render(self)


@crom.adapter
@crom.sources(IInlineForm, Interface)
@crom.target(ITemplate)
def default_form_template(component, request):
    """Default tempalte for ViewletForm
    """
    path = os.path.join(os.path.dirname(__file__), 'default_templates')
    return TALTemplate(os.path.join(path, 'formtemplate.pt'))
