from django.template import TemplateSyntaxError, Library, \
                            VariableDoesNotExist, Node, Variable
from django.conf import settings
from django.core.urlresolvers import reverse#, NoReverseMatch
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, Resolver404, get_resolver

from main import navigation

register = Library()


def process_links(links, view_name, url):
    items = []
    active_item = None
    for item, count in zip(links, range(len(links))):
        item_view = 'view' in item and item['view']
        item_url = 'url' in item and item['url']
        if view_name == item_view or url == item_url:
            active = True
            active_item = item
        else:
            active = False
            if 'links' in item:
                for child_link in item['links']:
                    child_view = 'view' in child_link and child_link['view']
                    child_url = 'url' in child_link and child_link['url']
                    if view_name == child_view or url == child_url:
                        active = True
                        active_item = item                
            
        items.append(
            {
                'first':count==0,
                'active':active,
                'url':item_view and reverse(item_view) or item_url or '#',
                'text':unicode(item['text']),
                'famfam':'famfam' in item and item['famfam'],
            }
        )
    return items, active_item


class NavigationNode(Node):
    def __init__(self, navigation, *args, **kwargs):
        self.navigation = navigation
        
    def render(self, context):
        request = Variable('request').resolve(context)
        view_name = resolve_to_name(request.META['PATH_INFO'])

        main_items, active_item = process_links(links=self.navigation, view_name=view_name, url=request.META['PATH_INFO'])
        context['navigation_main_links'] = main_items
        if active_item and 'links' in active_item:
            secondary_links, active_item = process_links(links=active_item['links'], view_name=view_name, url=request.META['PATH_INFO'])
            context['navigation_secondary_links'] = secondary_links
        return ''                


@register.tag
def main_navigation(parser, token):
    args = token.split_contents()

#    if len(args) != 3 or args[1] != 'as':
#        raise TemplateSyntaxError("'get_all_states' requires 'as variable' (got %r)" % args)

    #return NavigationNode(variable=args[2], navigation=navigation)    
    return NavigationNode(navigation=navigation)    


#http://www.djangosnippets.org/snippets/1378/
__all__ = ('resolve_to_name',)

def _pattern_resolve_to_name(self, path):
        match = self.regex.search(path)
        if match:
                name = ""
                if self.name:
                        name = self.name
                elif hasattr(self, '_callback_str'):
                        name = self._callback_str
                else:
                        name = "%s.%s" % (self.callback.__module__, self.callback.func_name)
                return name

def _resolver_resolve_to_name(self, path):
        tried = []
        match = self.regex.search(path)
        if match:
                new_path = path[match.end():]
                for pattern in self.url_patterns:
                        try:
                                name = pattern.resolve_to_name(new_path)
                        except Resolver404, e:
                                tried.extend([(pattern.regex.pattern + '   ' + t) for t in e.args[0]['tried']])
                        else:
                                if name:
                                        return name
                                tried.append(pattern.regex.pattern)
                raise Resolver404, {'tried': tried, 'path': new_path}


# here goes monkeypatching
RegexURLPattern.resolve_to_name = _pattern_resolve_to_name
RegexURLResolver.resolve_to_name = _resolver_resolve_to_name

def resolve_to_name(path, urlconf=None):
    return get_resolver(urlconf).resolve_to_name(path)

@register.filter
def resolve_url_name(value):
    return resolve_to_name(value)
