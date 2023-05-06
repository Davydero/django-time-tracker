def populate_models(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission, User
    from django.shortcuts import get_object_or_404
    # create groups
    # debemos anadir logica para que se ejecute solo una vez
    name1 = 'boss'
    name2 = 'worker'
    try:
        group1a = get_object_or_404(Group, name=name1)
        group2a = get_object_or_404(Group, name=name2)
        if group1a and group2a:
            print('Groups already exist')

    except:
        group1 = Group(name=name1)
        group1.save()
        group2 = Group(name=name2)
        group2.save()
        print('Groups created')
    
