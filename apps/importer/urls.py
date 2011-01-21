from django.conf.urls.defaults import *
from forms import PreviewForm, ExpressionForm, ImportWizard

urlpatterns = patterns('importer.views',
    url(r'^upload/$', 'import_file', (), 'import_wizard'),
    url(r'^wizard/$', 'import_wizard', (), 'import_next_steps'),
    url(r'^download_last_settings/$', 'download_last_settings', (), 'download_last_settings'),
)


