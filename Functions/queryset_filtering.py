from django.db.models import Q

def queryset_filtering(model, queries):
    filters = Q()
    all_fields = [x.name for x in model._meta.fields]
    queries_fields = []
    for field in queries.keys():
        for x in all_fields:
            if x in field:
                queries_fields.append(field)

    for key in queries_fields:
        q = Q(**{"%s" % key: queries.get(key)})
        filters &= q
    return filters