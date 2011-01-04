from django.template.defaultfilters import stringfilter
from django.template import Library, Node, Variable
from django.core.urlresolvers import reverse

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


'''
from django.contrib.auth.decorators import _CheckLogin

from inventory.views import *
from inventory.urls import urlpatterns

@register.filter
def login_required(value):
    for url in urlpatterns:
#		print "%s - %s - %s" % (value, url.name, url._get_callback())
        view_name = url._get_callback().__name__
        if value == url.name:
            try:
#				print eval(url._get_callback().__name__ +'.__class__')
                return eval(view_name +'.__class__') == _CheckLogin
            except:
                #unable to compare - missing import?
#				print "FALSE"
                return None
'''        
        
#	raise TemplateSyntaxError("%s" % item_detail.__class__)
        
'''from django.template import Node, Variable
from django.template import TemplateSyntaxError, Library, VariableDoesNotExist
from django.conf import settings

register = Library()

class URLNode(Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import reverse, NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        
        try:
            val1 = Variable(self.view_name).resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('Variable: "%s" does not exist' % self.view_name)
            #val1= None
                    
        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail, 
        # re-raise the NoReverseMatch unless we're using the 
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
#			url = reverse(self.view_name, args=args, kwargs=kwargs)
            url = reverse(val1, args=args, kwargs=kwargs)
        except NoReverseMatch:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            try:
                url = reverse(project_name + '.' + val1,
                              args=args, kwargs=kwargs)
            except NoReverseMatch:
                if self.asvar is None:
                    raise
                    register = Library()
        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

def url_dynamic(parser, token):
    bits = token.contents.split(' ')
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    asvar = None
        
    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))
    return URLNode(viewname, args, kwargs, asvar)
url_dynamic = register.tag(url_dynamic)

class URLNode_dynarg(Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import reverse, NoReverseMatch
#		args = [arg.resolve(context) for arg in self.args]
        args = [Variable(arg.resolve(context)).resolve(context) for arg in self.args]
#		args=[]
#		for arg in self.args:
#			resolved = arg.resolve(context)
#			print resolved
#			#args.append( Variable((arg.resolve(context))).resolve(context)  )
#			args.append(Variable(resolved).resolve(context))
        
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        try:
            val1 = Variable(self.view_name).resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('Variable: "%s" does not exist' % self.view_name)
            #val1= None
                    
        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail, 
        # re-raise the NoReverseMatch unless we're using the 
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
#			url = reverse(self.view_name, args=args, kwargs=kwargs)
            url = reverse(val1, args=args, kwargs=kwargs)
        except NoReverseMatch:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            try:
                url = reverse(project_name + '.' + val1,
                              args=args, kwargs=kwargs)
            except NoReverseMatch:
                if self.asvar is None:
                    raise
                    register = Library()
        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

def url_dynamic_full(parser, token):
    bits = token.contents.split(' ')
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    asvar = None
        
    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))
    return URLNode_dynarg(viewname, args, kwargs, asvar)
url_dynamic_full = register.tag(url_dynamic_full)
'''
