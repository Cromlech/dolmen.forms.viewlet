"""

We define a viewlet form here.

Let's grok our example:

  >>> from dolmen.forms.viewlet.testing import grok
  >>> grok('dolmen.forms.viewlet.ftests.forms.viewlet')

Let's render the view that use our viewlet now:

  >>> from cromlech.io.testing import TestRequest
  >>> from dolmen.forms.viewlet.ftests.forms import viewlet as test

  >>> request = TestRequest()
  >>> context = test.Context()
  >>> page = test.Index(context, request)
  >>> manager = test.Manager(context, request, page)
  >>> print manager()
  <form method="post" enctype="multipart/form-data" id="form">
    <h3>Subscription corner</h3>
    <div class="fields">
      <div class="field">
        <label class="field-label" for="form-field-name">Name</label>
        <br />
        <input type="text" id="form-field-name" name="form.field.name" class="field" value="" />
      </div>
      <div class="field">
        <label class="field-label" for="form-field-email">Email</label>
        <br />
        <input type="text" id="form-field-email" name="form.field.email" class="field" value="" />
      </div>
    </div>
    <div class="actions">
      <div class="action">
        <input type="submit" id="form-action-subscribe" name="form.action.subscribe" value="Subscribe" class="action" />
      </div>
    </div>
  </form>


Integration tests
-----------------

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
    <form method="post" enctype="multipart/form-data" id="form">
      <h3>Subscription corner</h3>
      <div class="fields">
        <div class="field">
          <label class="field-label" for="form-field-name">Name</label>
          <br />
          <input type="text" id="form-field-name" name="form.field.name" class="field" value="" />
        </div> <div class="field">
          <label class="field-label" for="form-field-email">Email</label>
          <br />
          <input type="text" id="form-field-email" name="form.field.email" class="field" value="" />
        </div>
      </div>
      <div class="actions">
        <div class="action">
          <input type="submit" id="form-action-subscribe" name="form.action.subscribe" value="Subscribe" class="action" />
        </div>
      </div>
    </form>
  </div>

  >>> 'Registration done for Grok' not in browser.contents
  True

  >>> form = browser.get_form(id='form')
  >>> form.get_control('form.field.name').value = 'Grok'
  >>> form.get_control('form.field.email').value = 'grok@zope.org'
  >>> form.get_control('form.action.subscribe').click()
  200
  >>> 'Registration done for Grok' in browser.contents
  True

"""

from os import path
from cromlech.webob.response import Response
from dolmen.forms.base import Field, Fields, action, FAILURE, SUCCESS
from dolmen.forms.viewlet import ViewletForm
from dolmen.tales import SlotExpr
from dolmen.template import TALTemplate
from dolmen.view import View
from dolmen.viewlet import ViewletManager
from dolmen.viewlet import name, slot, context, view


PATH = path.join(path.dirname(__file__), 'templates')


class Template(TALTemplate):
    expression_types = {'slot': SlotExpr}


class Context(object):
    pass


class Index(View):
    context(Context)
    responseFactory = Response
    template = Template(path.join(PATH, 'viewlet.pt'))


class Manager(ViewletManager):
    name('manager')
    view(Index)
    context(Context)


class Form(ViewletForm):
    view(Index)
    slot(Manager)
    context(Context)

    label = 'Subscription corner'
    fields = Fields(Field('Name'), Field('Email'))

    @action("Subscribe")
    def subscribe(self):
        data, errors = self.extractData()
        if errors:
            return FAILURE
        self.status = "Registration done for %s" % (data['name'])
        return SUCCESS
