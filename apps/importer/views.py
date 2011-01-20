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
    wizard = ImportWizard(form_list=[PreviewForm, ExpressionFormSet, ImportResultForm])
    return wizard(request)
    
   
def import_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
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
        form = DocumentForm()


    return render_to_response('generic_form.html', {
        'form':form,
        'title':_(u'Upload a file to import'),
    },
    context_instance=RequestContext(request))    
   
    
'''
def import_file(request):
    title = ''
    hidden_fields = {}
    formset = None
    step = int(request.POST.get('step', 1))
    if request.method == 'POST':
        if step == 1:
            title = _(u'Upload a file to import')
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                title = _(u'File preview')
                hidden_fields['step'] = 2               
                hidden_fields['model_name'] = form.cleaned_data['model_name']                
                temp_file = handle_uploaded_file(form.cleaned_data['local_document'])
                form = prepare_preview_form(temp_file)
                hidden_fields['temp_file'] = temp_file

        if step == 2:
            temp_file = request.POST.get('temp_file', None)
            model_name = request.POST.get('model_name', None)
            app_label, name = model_name.split('.')
            ct = ContentType.objects.get(app_label=app_label, name=name)
            model = ct.model_class()
            ExpressionFormSet = formset_factory(ExpressionForm, extra=0)
            initial=[]
            for num, field in zip(range(len(model._meta.fields)), model._meta.fields):
                if field.name != 'id':
                    initial.append({
                        'model_field':field.name,
                        'expression':'"%%s" %% row.column[%s]' % str(num-1),
                        'enabled':(field.name != 'id' and True)
                        })
            formset = ExpressionFormSet(initial=initial)
            form = None
            hidden_fields['step'] = 3
            hidden_fields['model_name'] = model_name
            hidden_fields['temp_file'] = temp_file
        if step == 3:
            temp_file = request.POST.get('temp_file', None)
            model_name = request.POST.get('model_name', None)
            app_label, name = model_name.split('.')
            ct = ContentType.objects.get(app_label=app_label, name=name)
            model = ct.model_class()
            perform_import(model, temp_file)
            
    else:
        title = _(u'Upload a file to import')
        form = DocumentForm()
        hidden_fields['step'] = 1

    return render_to_response('generic_form.html', {
        'hidden_fields':hidden_fields,
        'form':form,
        'formset':formset,
        'title':title,
    },
    context_instance=RequestContext(request))    
'''
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
