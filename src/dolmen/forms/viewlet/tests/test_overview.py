# -*- coding: utf-8 -*-


import dolmen.forms.base
import crom
from os import path
from crom import testing
from cromlech.browser.testing import XMLDiff, TestRequest, TestResponse
from dolmen.forms.base import Field, Fields, action, FAILURE, SUCCESS
from dolmen.forms.viewlet import ViewletForm
from dolmen.template import TALTemplate
from dolmen.view import View
from dolmen.viewlet import ViewletManager
from dolmen.viewlet import name, slot, context, view


PATH = path.dirname(__file__)


class Context(object):
    pass


class Index(View):
    context(Context)
    responseFactory = TestResponse
    template = TALTemplate(path.join(PATH, 'viewlet.pt'))


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


def setup_function(module):
    testing.setup()
    from . import test_overview
    import dolmen.forms.base
    crom.configure(dolmen.forms.base)
    crom.configure(dolmen.forms.viewlet)
    crom.configure(test_overview)


def teardown_function(module):
    testing.teardown()


def test_viewlet_manager():
  request = TestRequest()
  context = Context()
  page = Index(context, request)
  manager = Manager(context, request, page)
  viewlet = Form(context, request, page, manager)

  viewlet.update()
  assert not XMLDiff(viewlet.render(), EXPECTED)


EXPECTED = """<form action="." method="post" enctype="multipart/form-data" id="form">
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
    </form>"""
