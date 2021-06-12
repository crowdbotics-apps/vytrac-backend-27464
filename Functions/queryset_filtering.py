from django.db.models import Q

from Functions.debuging import Debugging


def queryset_filtering(model, queries):
    filters = Q()
    all_fields = [x.name for x in model._meta.get_fields()]

    queries_fields = []
    for field in queries.keys():
        for x in all_fields:
            if x in field:
                queries_fields.append(field)

    for key in queries_fields:
        q = Q(**{"%s" % key: queries.get(key)})
        filters &= q
    Model = model.objects.filter(Q(filters))
    latest = queries.get('latest')
    earliest = queries.get('earliest')
    if latest:
        Model = [Model.latest()]
    if earliest:
        Model = [Model.earliest()]
    return Model