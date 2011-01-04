from django.conf.urls.defaults import *

from inventory.models import Person, Item, ItemTemplate, RetiredItem

urlpatterns = patterns('main.views',
    url(r'^set_language/$', 'set_language', (), 'set_language'),
    url(r'^test/$', 'test', (), 'test'),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', { 'template' : 'home.html', 'extra_context' : { 'person': Person.objects.all(), 'item': Item.objects.all(), 'template': ItemTemplate.objects.all(), 'retired' : RetiredItem.objects.all() }}, "home"),
#    (r'^$', 'direct_to_template', { 'template' : 'home.html'}, "home"),
)
