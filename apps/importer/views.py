import os
import csv
import tempfile

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.simplejson import dumps, loads
from django.utils.http import urlencode


from forms import DocumentForm, PreviewForm, ExpressionForm, ImportResultForm, ImportWizard

def handle_uploaded_file(f):
    destination, filepath = tempfile.mkstemp()

    destination = open(filepath, 'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return filepath
   
   
def import_wizard(request):
    ExpressionFormSet = formset_factory(ExpressionForm, extra=0)
    ExpressionFormSet.title = _(u'expressions')
    wizard = ImportWizard(form_list=[PreviewForm, ExpressionFormSet, ImportResultForm, ImportResultForm])
    return wizard(request)
    
   
def import_file(request):
    models = [
        'inventory.inventory',
        'inventory.inventorytransaction',
        'assets.itemgroup',
        'assets.itemstate',
        'inventory.itemtemplate', 
        'inventory.location',
        'assets.person',
        'assets.state',
        'inventory.supplier',
        'assets.item',
    ]
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, models=models)
        if form.is_valid():
            temp_file = handle_uploaded_file(form.cleaned_data['local_document'])
            return HttpResponseRedirect(
                '?'.join(
                    [reverse('import_next_steps'),
                     urlencode({
                        'temp_file':temp_file,
                        'model_name':form.cleaned_data['model_name'],
                    })]))
         
    else:
        form = DocumentForm(models=models)


    return render_to_response('generic_form.html', {
        'form':form,
        'title':_(u'Upload a file to import'),
    },
    context_instance=RequestContext(request))    
    
    
def download_last_settings(request):
    settings = request.session.get('last_import_settings', None)
    if settings:
        content=dumps(settings)
        response = HttpResponse(content, content_type='text/plain', mimetype='application/json')
        response['Content-Length'] = len(content)
        response['Content-Disposition'] = "attachment; filename=last_import_settings.json"
        return response
                       

    messages.error(request, _(u'There are no settings available to download.'))
    return HttpResponseRedirect('/')
