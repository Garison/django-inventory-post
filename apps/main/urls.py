from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    url(r'^set_language/$', 'set_language', (), 'set_language'),
)
