from django.template.defaultfilters import stringfilter
from django.template import Library, Node, Variable
from django.core.urlresolvers import reverse

from assets.models import State

register = Library()


class GetAllStatesNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        context[self.variable] = State.objects.all()
        return ''


@register.tag
def get_all_states(parser, token):
    args = token.contents.split()
    if len(args) != 3 or args[1] != 'as':
        raise TemplateSyntaxError("'get_all_states' requires 'as variable' (got %r)" % args)
    return GetAllStatesNode(args[2])
