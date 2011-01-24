import types

object_navigation = {}

def register_links(src, links, menu_name=None):
    if isinstance(src, (types.TupleType, types.ListType)):
        for one_src in src:
            object_navigation.update({one_src:{'links':links, 'menu_name':menu_name}})
    else:
        object_navigation.update({src:{'links':links, 'menu_name':menu_name}})


