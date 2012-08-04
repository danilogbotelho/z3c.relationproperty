z3c.relationproperty
**********************

Introduction
============

This product aims at making the use of `z3c.relationfield`_ relations
more transparent and also easier.

.._`z3c.relationfield`:http://pypi.python.org/pypi/z3c.relationfield

The regular use of z3c.relationfield suggests that a relation be
created in a schema and that all subsequent uses of the object linked
to be made though the relation's to_object attribute. That adds an
extra burden as mentioned `here`_.

.._`here`:http://grok.zope.org/documentation/how-to/using-a-relationfield-for-relationships-between/


Setup
=====

  >>> from z3c.relationfield import Relation
  >>> from zope.interface import Interface

Define the schema::

  >>> class IBuddy(Interface, IHasRelations):
  ...   name = schema.TextLine(title=u'The Name')
  ...   buddy = schema.Choice(
  ...      title=u'My Buddy',
  ...      required=False,
  ...      source = BuddySource())
  ...   taggedValue('buddy', Relation())

Create the model::

  >>> class Buddy(Persistent):
  ...   implements(IBuddy)
  ...   name = FieldProperty(IBuddy['name'])
  ...   buddy = RelationProperty(IBuddy['buddy'])


Let's now test the application::

  >>> from zope.app.component.site import SiteManagerContainer
  >>> from zope.app.container.btree import BTreeContainer
  >>> class TestApp(SiteManagerContainer, BTreeContainer):
  ...   pass

We set up the test application::

  >>> root = getRootFolder()['root'] = TestApp()

We make sure that this is the current site, so we can look up local
utilities in it and so on. Normally this is done automatically by
Zope's traversal mechanism::

  >>> from zope.app.component.site import LocalSiteManager
  >>> root.setSiteManager(LocalSiteManager(root))
  >>> from zope.app.component.hooks import setSite
  >>> setSite(root)

For this site to work with ``z3c.relationship``, we need to set up two
utilities. Firstly, an ``IIntIds`` that tracks unique ids for objects
in the ZODB::

  >>> from zope.app.intid import IntIds
  >>> from zope.app.intid.interfaces import IIntIds
  >>> root['intids'] = intids = IntIds() 
  >>> sm = root.getSiteManager()
  >>> sm.registerUtility(intids, provided=IIntIds)

And secondly a relation catalog that actually indexes the relations::

  >>> from z3c.relationfield import RelationCatalog
  >>> from zc.relation.interfaces import ICatalog
  >>> root['catalog'] = catalog = RelationCatalog()
  >>> sm.registerUtility(catalog, provided=ICatalog)





