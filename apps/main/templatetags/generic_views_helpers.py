import types

from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.template import Library, Node, Variable, VariableDoesNotExist

register = Library()

class DynUrlNode(Node):
    def __init__(self, *args):
        self.name_var = Variable(args[0])
        if len(args)>1:
            #Process view arguments
            self.args = [Variable(a) for a in args[1].split(',')]
        else:
            self.args = []

    def render(self, context):
        name = self.name_var.resolve(context)
        args = [a.resolve(context) for a in self.args]
        try:
            return reverse(name, args = args)
        except:
            #Argument might be pointing to a context variable
            args = [Variable(a).resolve(context) for a in args]
            return reverse(name, args = args)


@register.tag
def dynurl(parser, token):
    args = token.split_contents()
    return DynUrlNode(*args[1:])


@register.filter
@stringfilter
def is_class(value, arg):
    return value[21:(value[21:].find(' ')+21)] == arg


def return_attrib(obj, attrib, arguments={}):
    try:
        if isinstance(obj, types.DictType) or isinstance(obj, types.DictionaryType):
            return obj[attrib]
        elif isinstance(attrib, types.FunctionType):
            return attrib(obj)
        else:
            result = reduce(getattr, attrib.split("."), obj)
            if isinstance(result, types.MethodType):
                if arguments:
                    return result(**arguments)
                else:
                    return result()
            else:
                return result
    except Exception, err:
        if settings.DEBUG:
            return "Error: %s; %s" % (attrib, err)
        else:
            pass

@register.filter
def object_property(value, arg):
    return return_attrib(value, arg)


from main import new_navigation

class GetNavigationLinks(Node):
    def __init__(self, *args):
        pass
        #self.name_var = Variable(args[0])
        #if len(args)>1:
        #    #Process view arguments
        #    self.args = [Variable(a) for a in args[1].split(',')]
        #else:
        #    self.args = []

    def render(self, context):
        context_links = []
        try:
            object_name = Variable('object_name').resolve(context)
        except VariableDoesNotExist:
            object_name = 'object'

        try:
            object = Variable(object_name).resolve(context)

            for id, links in new_navigation.items():
                if isinstance(object, id):
                    for link in links:
                        context_links.append(link)
        except VariableDoesNotExist:
            pass
                
                
        context['new_navigation_links'] = context_links
        return ''
            
        #name = self.name_var.resolve(context)
        #args = [a.resolve(context) for a in self.args]
        #try:
        #    return reverse(name, args = args)
        #except:
        #    #Argument might be pointing to a context variable
        #    args = [Variable(a).resolve(context) for a in args]
        #    return reverse(name, args = args)


@register.tag
def get_navigation_links(parser, token):
    #args = token.split_contents()
    return GetNavigationLinks()#*args[1:])
