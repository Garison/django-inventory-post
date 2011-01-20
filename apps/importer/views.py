import csv
import tempfile

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlencode


from forms import DocumentForm, PreviewForm, ExpressionForm, ImportResultForm, ImportWizard

def handle_uploaded_file(f):
    filepath = tempfile.mktemp()

    destination = open(filepath, 'wb+')
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
    models = ['assets.asset', 'assets.item_group', 'assets.item_state', 
            'assets.person', 'assets_state', 'inventory.inventory', 
            'inventory.inventory transaction', 'inventory.item_template', 
            'inventory.location', 'inventory.supplier'] 
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)#, models=models)
        if form.is_valid():
            temp_file = handle_uploaded_file(form.cleaned_data['local_document'])
            return HttpResponseRedirect(
                '?'.join(
                    [reverse('import_wizard'),
                     urlencode({
                        'temp_file':temp_file,
                        'model_name':form.cleaned_data['model_name'],
                    })]))
         
    else:
        form = DocumentForm()#models=models)


    return render_to_response('generic_form.html', {
        'form':form,
        'title':_(u'Upload a file to import'),
    },
    context_instance=RequestContext(request))    
   
'''

def prepare_preview_form(filepath):
    csvfile = open(filepath, 'rb')
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    print 'delimiter', dialect.delimiter
    print 'doublequote', dialect.doublequote
    print 'escapechar', dialect.escapechar
    print 'lineterminator', dialect.lineterminator
    print 'quotechar', dialect.quotechar
    print 'quoting', dialect.quoting
    csvfile.seek(0)

    return PreviewForm(initial={'preview_area':''.join([csvfile.readline() for i in range(10)])})
'''    
   
'''
def perform_import(model, datafile):
    #print 'datafile', datafile
    csvfile = open(datafile, 'rb')
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    
    reader = csv.reader(open(datafile, 'r'), dialect=dialect)#dialect='excel')
   
    for row in reader:
        
        print row[0], row[1]
        #model.objects.get_or_create(MY_FIRST_COLUMN=COLUMN_ONE_TITLE, MY_SECOND_COLUMN=COLUMN_TWO_TITLE)
'''      
        
        
#    try:
#        csvfile = file(datafile, 'r')
#    except IOError:
#        self.error('Could not open specified csv file, %s, or it does not exist' % datafile, 0)
#    else:
#        # CSV Reader returns an iterable, but as we possibly need to
#        # perform list commands and since list is an acceptable iterable, 
#        # we'll just transform it.
#        return list(csv.reader(csvfile))



   
    

#https://github.com/girasquid/django-csv-importer
'''
    def __csvfile(self, datafile):
        try:
            csvfile = file(datafile, 'r')
        except IOError:
            self.error('Could not open specified csv file, %s, or it does not exist' % datafile, 0)
        else:
            # CSV Reader returns an iterable, but as we possibly need to
            # perform list commands and since list is an acceptable iterable, 
            # we'll just transform it.
            return list(csv.reader(csvfile))

        if self.nameindexes:
            indexes = self.csvfile.pop(0)
            
        for row in self.csvfile:

'''

'''
import sys
from django.core.management import setup_environ
sys.path.append(LOCATION OF YOUR DJANGO PROJECTS, EX: 'C:\django')
from mysite import settings
setup_environ(settings)

from PROJECT_NAME.APP_NAME.models import MODEL_NAME

import csv
reader = csv.reader(open(COMPLETE PATH TO YOUR DATA, EX: "C:/django/mysite/restaurants.csv"), dialect='excel')
   
for row in reader:
   COLUMN_ONE_TITLE = row[0]
   COLUMN_TWO_TITLE = row[1]
                      
   MODEL_NAME.objects.get_or_create(MY_FIRST_COLUMN=COLUMN_ONE_TITLE, MY_SECOND_COLUMN=COLUMN_TWO_TITLE)

to python dja
'''
