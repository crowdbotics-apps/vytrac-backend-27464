

def make_fields_permissions(Model):
    mode_name = Model.__name__.lower()
    permissions = []
    for item in Model._meta.fields:
        permissions.append(('view_'+mode_name+'.'+item.name+'_field',
                            'Can view '+item.name.replace('_', ' ')))

    for item in Model._meta.fields:
        permissions.append(('change_'+mode_name+'.'+item.name+'_field',
                            'Can change '+item.name.replace('_', ' ')))
    return permissions
