from django.conf.urls.defaults import *
from forms import PreviewForm, ExpressionForm, ImportWizard

urlpatterns = patterns('importer.views',
    url(r'^import/$', 'import_file', (), 'import'),
    url(r'^import_wizard/$', 'import_wizard', (), 'import_wizard'),
)

#urlpatterns += patterns('',
#    url(r'^import_wizard/$', ImportWizard([PreviewForm, ExpressionForm]), name='import_wizard'),
#)

