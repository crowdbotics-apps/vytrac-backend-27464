
def fields_lookups(MyModel):
    lookups = {}

    fields = [x.name for x in MyModel._meta.fields]
    for field in fields:
        lookups[field] = [*MyModel._meta.get_field(
            field).get_lookups().keys()]
    return lookups
