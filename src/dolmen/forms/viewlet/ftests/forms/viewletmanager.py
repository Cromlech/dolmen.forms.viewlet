"""

We define a viewlet manager form here.

Let's grok our example:

  >>> from dolmen.forms.viewlet.testing import grok
  >>> grok('dolmen.forms.viewlet.ftests.forms.viewletmanager')


Integration tests
-----------------

  >>> from cromlech.io.testing import TestRequest
  >>> from dolmen.forms.viewlet.ftests.forms import viewletmanager as test
  
  >>> request = TestRequest()
  >>> context = test.Context()

  >>> context.__name__ = 'content'
  >>> context.__parent__ = getRootFolder()

  >>> from infrae.testbrowser.browser import Browser
  >>> app = makeApplication(context, 'index')
  >>> browser = Browser(app)
  >>> browser.handleErrors = False

Submission
~~~~~~~~~~

We are going just to submit the form without giving any required
information, and we should get an error:

  >>> browser.open('http://localhost/content/index')
  200
  >>> print browser.contents
  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
  <div>
    <form method="post" enctype="multipart/form-data" id="registration">
      <h3>Subscription corner</h3>
      <div class="fields">
        <div class="field">
          <label class="field-label" for="registration-field-name">Name</label>
          <br />
          <input type="text" id="registration-field-name" name="registration.field.name" class="field" value="" />
        </div> <div class="field">
          <label class="field-label" for="registration-field-email">Email</label>
          <br />
          <input type="text" id="registration-field-email" name="registration.field.email" class="field" value="" />
        </div>
      </div>
      <div class="actions">
        <div class="action">
          <input type="submit" id="registration-action-subscribe" name="registration.action.subscribe" value="Subscribe" class="action" />
        </div>
      </div>
    </form>
  </div>

  >>> 'Registration done for Grok' not in browser.contents
  True

  >>> form = browser.get_form(id='registration')
  >>> form.get_control('registration.field.name').value = 'Grok'
  >>> form.get_control('registration.field.email').value = 'grok@zope.org'
  >>> form.get_control('registration.action.subscribe').click()
  200
  >>> 'Registration done for Grok' in browser.contents
  True

"""

from os import path
from cromlech.webob.response import Response
from dolmen.forms.base import Field, Fields, action, FAILURE, SUCCESS
from dolmen.forms.viewlet import ViewletManagerForm
from dolmen.tales import SlotExpr
from dolmen.template import TALTemplate
from dolmen.view import View
from dolmen.viewlet import context, view


PATH = path.join(path.dirname(__file__), 'templates')


class Template(TALTemplate):
    expression_types = {'slot': SlotExpr}


class Context(object):
    pass


class Index(View):
    context(Context)
    responseFactory = Response

    template = Template(path.join(PATH, 'manager.pt'))


class Registration(ViewletManagerForm):
    context(Context)
    view(Index)

    label = 'Subscription corner'
    fields = Fields(Field('Name'), Field('Email'))
    responseFactory = Response

    @action("Subscribe")
    def subscribe(self):
        data, errors = self.extractData()
        if errors:
            return FAILURE
        self.status = "Registration done for %s" % (data['name'])
        return SUCCESS
