from django.conf.urls.defaults import *


urlpatterns = patterns('photos.views',
    url(r'^(?P<object_id>\d+)/delete/$', 'generic_photo_delete', (), 'generic_photo_delete'),
    url(r'^(?P<object_id>\d+)/mark_as_main/$', 'generic_photo_mark_main', (), 'generic_photo_mark_main')
)
    

