from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue


def iid(obj):
    intids = getUtility(IIntIds)
    return intids.getId(obj)


def iid2obj(iid):
    intids = getUtility(IIntIds)
    return intids.getObject(iid)


def obj2rel(obj):
    return RelationValue(iid(obj))
