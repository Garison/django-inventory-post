from django.conf.urls.defaults import *

urlpatterns = patterns('importer.views',
    url(r'^import/$', 'import_file', (), 'import'),
)

#urlpatterns = patterns('',
#    url(r'^import/$', ImportWizard([DocumentForm, DialectForm]), name='import'),
#)

