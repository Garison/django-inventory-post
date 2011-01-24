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
