from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

from inventory.admin import mysite

urlpatterns = patterns('',
    #----Django
    (r'^orig_admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^orig_admin/(.*)', admin.site.root),
    (r'^admin/(.*)', mysite.root),
    (r'^i18n/', include('django.conf.urls.i18n')),
    
    #----Project
    (r'^inventory/', include('inventory.urls')),
    (r'^', include('main.urls')),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', { 'template' : 'about.html'}, 'about'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='user_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : "/"}, name='user_logout' ),
    url(r'^myaccount/password_change/$', 'django.contrib.auth.views.password_change', name='user_me_password_change'),
    url(r'^accounts/password_change_ok/$', 'django.contrib.auth.views.password_change_done')
)

if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'site_media', 'show_indexes': True}),
    )

