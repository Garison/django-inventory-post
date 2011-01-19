import csv

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.files.uploadhandler import TemporaryFileUploadHandler

from forms import DocumentForm, DialectForm#, ImportWizard

def handle_uploaded_file(f):
    filepath='/tmp/test.csv'

    destination = open(filepath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return filepath
    

def import_file(request):
    title = ''
 
    file_to_import = request.session.get('file_to_import', False)
    #setattr(settings, 'FILE_UPLOAD_HANDLERS', ("django.core.files.uploadhandler.TemporaryFileUploadHandler",))
    if request.method == 'POST':
        #if not request.FILES:
        #    request.upload_handlers = [TemporaryFileUploadHandler()]
        
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            temp_file = handle_uploaded_file(form.cleaned_data['local_document'])
            #print 'FILES',  form.cleaned_data['local_document'].name
            request.session['file_to_import'] = '2'
            form = sniff_file(temp_file)
            #print 'form', form
            title = _(u'File preview')

    else:
        title = _(u'Upload a file to import')
        form = DocumentForm()

    return render_to_response('generic_form.html', {
        'form':form,
        'title':title,
    },
    context_instance=RequestContext(request))    


def sniff_file(filepath):
    csvfile = open(filepath, 'rb')
    #csvfile = file_field.file
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    preview = {}
    #for i in range(1,5):
    #    preview['preview_line_%s' % i] = csvfile.readline()
    
    
    #print [csvfile.readline() for i in range(4)]
    return DialectForm(initial={'preview_area':'\n'.join([csvfile.readline() for i in range(4)])})#
    #.join([line for i,line in range(4),csvfile.readline()])})
    
    #print 'preview', preview
    #print dialect.delimiter


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
