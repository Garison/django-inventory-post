from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import django.contrib.auth.views


urlpatterns = patterns('common.views',
    url(r'^set_language/$', 'set_language', (), 'set_language'),
    url(r'^about/$', direct_to_template, { 'template' : 'about.html'}, 'about'),
    url(r'^login/$', django.contrib.auth.views.login, name='user_login'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page' : "/"}, name='user_logout' ),
    url(r'^myaccount/password_change/$', django.contrib.auth.views.password_change, name='user_me_password_change'),
    url(r'^accounts/password_change_ok/$', django.contrib.auth.views.password_change_done)    
)
