from zope.interface import providedBy
from zope.schema import getFields
from z3c.relationfield.interfaces import IRelation, IRelationList


def _potential_relations(obj):
    """Given an object return tuples of name, index, relation value.

    Returns both IRelationValue attributes as well as ITemporaryRelationValue
    attributes.

    If this is a IRelationList attribute, index will contain the index
    in the list. If it's a IRelation attribute, index will be None.
    """
    for iface in providedBy(obj).flattened():
        for name, field in getFields(iface).items():
            print '**', name
            frel = name + '_rel'
            _rel = iface.queryTaggedValue(frel)
            if _rel is not None:
                field = _rel
                name = frel
                print '>>>>', name, field, _rel

            if IRelation.providedBy(field):
                try:
                    relation = getattr(obj, name)
                except AttributeError:
                    # can't find this relation on the object
                    continue
                yield name, None, relation
            if IRelationList.providedBy(field):
                try:
                    l = getattr(obj, name)
                except AttributeError:
                    # can't find the relation list on this object
                    continue
                if l is not None:
                    for i, relation in enumerate(l):
                        yield name, i, relation
