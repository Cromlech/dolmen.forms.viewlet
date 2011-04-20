# -*- coding: utf-8 -*-

import cromlech.webob.request
import doctest
import dolmen.forms.base
import unittest
import webob.dec

from cromlech.io.interfaces import IPublicationRoot
from pkg_resources import resource_listdir
from zope.component import getMultiAdapter
from zope.component.testlayer import LayerBase
from zope.interface import Interface, directlyProvides
from zope.location import Location


class WSGIApplication(object):

    def __init__(self, context, viewname):
        self.context = context
        self.viewname = viewname

    @webob.dec.wsgify(RequestClass=cromlech.webob.request.Request)
    def __call__(self, req):
        form = getMultiAdapter(
            (self.context, req), Interface, self.viewname)
        return form()


class BrowserLayer(LayerBase):

    def setUp(self):
        LayerBase.setUp(self)
        context = Location()
        directlyProvides(context, IPublicationRoot)
        self.root = context

    def getRootFolder(self):
        return self.root

    def makeApplication(self, context, viewname):
        return WSGIApplication(context, viewname)


FunctionalLayer = BrowserLayer(dolmen.forms.base)


def suiteFromPackage(name):
    optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    globs = {'getRootFolder': FunctionalLayer.getRootFolder,
             'makeApplication': FunctionalLayer.makeApplication}
    
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'dolmen.forms.viewlet.ftests.%s.%s' % (name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname, optionflags=optionflags, globs=globs)
        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['forms']:
        suite.addTest(suiteFromPackage(name))
    suite.layer = FunctionalLayer
    return suite
