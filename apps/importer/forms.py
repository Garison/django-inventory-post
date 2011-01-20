import os
import csv

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.simplejson import dumps, loads
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from api import perform_import
from wizard import BoundFormWizard

#TODO: Allow row 0 to be used as column names
#TODO: Save mapping
'''import os, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


def send_file(request):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """
    filename = __file__ # Select your file here.                                
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response
    
  lat = float(request.GET.get('lat'))
lng = float(request.GET.get('lng'))
a = Authority.objects.get(area__contains=Point(lng, lat))
if a:
    return HttpResponse(simplejson.dumps({'name': a.name, 
                                          'area': a.area.geojson,
                                          'id': a.id}), 
                        mimetype='application/json')  
'''
#TODO: remove spaces in model names
#TODO: Load mapping in step 0
#TODO: Allow user to tweak dialect in preview 
#TODO: Close & delete temp file
#Ticket #7439 (new) FormWizard don't process multipart forms
#Ticket #11112 (new) Formsets not supported as steps in FormWizard   - DONE

class DocumentValidationError(forms.ValidationError):
    def __init__(self):
        msg = _(u'Only CSV files are valid uploads.')
        super(DocumentValidationError, self).__init__(msg)


class DocumentField(forms.FileField):
    """A validating PDF document upload field"""

    def clean(self, data, initial=None):
        f = super(DocumentField, self).clean(data, initial)
        ext = os.path.splitext(f.name)[1][1:].lower()

        if ext == 'csv' and f.content_type == 'text/csv':
            return f
        raise DocumentValidationError()


class DocumentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        models = kwargs.pop('models', [])
        if models:
            choices = models
        else:
            qs=ContentType.objects.all()
            choices = sorted(["%s.%s" % (model.app_label, model.name) for model in qs])

        exclude = kwargs.pop('exclude', [])
        for exclusion in exclude:
            choices.remove(exclusion)

        super(DocumentForm, self).__init__(*args, **kwargs)
            
        self.fields['model_name'].choices=zip(choices, choices)
        
    local_document = DocumentField(label=_(u'Local document'))
    model_name = forms.ChoiceField(label=_(u'Model'), help_text=_(u'Model that will receive the data.'))
    #import_mappings = forms.FileField(label=_(u'Import mappings file (optional)'), required=False)


class PreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.title = _(u'import preview')
        super(PreviewForm, self).__init__(*args, **kwargs)
            
    preview_area = forms.CharField(label=_(u'Preview'), required=False, widget=forms.widgets.Textarea(attrs={'cols':80, 'rows':10}))
    discard_firstrow = forms.BooleanField(label=_(u'Discard first row'), required=False)

    dialect_delimiter = forms.CharField(label=_('Delimiter'), help_text=_(u'A one-character string used to separate fields. It defaults to ",".'))
    dialect_doublequote = forms.BooleanField(label=_('Doublequote'), required=False, help_text=_(u'Controls how instances of quotechar appearing inside a field should be themselves be quoted. When True, the character is doubled. When False, the escapechar is used as a prefix to the quotechar. It defaults to True.'))
    dialect_escapechar = forms.CharField(label=_('Escape character'), required=False, help_text=_(u'A one-character string used by the writer to escape the delimiter if quoting is set to QUOTE_NONE and the quotechar if doublequote is False. On reading, the escapechar removes any special meaning from the following character. It defaults to None, which disables escaping.'))
    dialect_lineterminator = forms.CharField(label=_('Line terminator'), required=False, help_text=_(u'The string used to terminate lines produced by the writer. It defaults to "\\r\\n".'))
    dialect_quotechar = forms.CharField(label=_('Quote character'), help_text=_(u'A one-character string used to quote fields containing special characters, such as the delimiter or quotechar, or which contain new-line characters. It defaults to ".'))
    dialect_quoting = forms.CharField(label=_('Quoting'), required=False, help_text=_(u'Controls when quotes should be generated by the writer and recognised by the reader.'))
    dialect_skipinitialspace = forms.BooleanField(label=_('Skip initial space'), required=False, help_text=_(u'When True, whitespace immediately following the delimiter is ignored. The default is False.'))


class ExpressionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExpressionForm, self).__init__(*args, **kwargs)

    model_field = forms.CharField(label=_(u'Model field'))
    expression = forms.CharField(label=_(u'Expression'))
    arguments = forms.CharField(label=_(u'Arguments'), required=False)
    enabled = forms.BooleanField(label=_(u'Enabled'), required=False)


class ImportResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        title = _(u'import results')
        if 'initial' in kwargs:
            if kwargs['initial']:
                title = kwargs['initial'].pop('title', _(u'import results'))
        
        self.title = title
        super(ImportResultForm, self).__init__(*args, **kwargs)
        
    result_area = forms.CharField(label=_(u'Results'), required=False, widget=forms.widgets.Textarea(attrs={'cols':80, 'rows':10}))
    

def save_settings(settings):
    return HttpResponse(simplejson.dumps(settings), 
                        mimetype='application/json')  
                            

class ImportWizard(BoundFormWizard):
    def parse_params(self, request, *args, **kwargs):
        self.temp_file = request.GET.get('temp_file', None)
        self.model_name = request.GET.get('model_name', None)

        csvfile = open(self.temp_file, 'rb')
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)

        self.initial = {0:
            {
                'preview_area':''.join([csvfile.readline() for i in range(10)]),
                'dialect_delimiter':dialect.delimiter,
                'dialect_doublequote':dialect.doublequote,
                'dialect_escapechar':dialect.escapechar,
                'dialect_lineterminator':dialect.lineterminator,
                'dialect_quotechar':dialect.quotechar,
                'dialect_quoting':dialect.quoting,
                'dialect_skipinitialspace':dialect.skipinitialspace,
            }
        }
        csvfile.close()
        
    def get_template(self, step):
        return 'import_wizard.html'
    
       
    def process_step(self, request, form, step):
        if step == 0:
            self.discard_firstrow = form.cleaned_data['discard_firstrow']
            app_label, name = self.model_name.split('.')
            ct = ContentType.objects.get(app_label=app_label, name=name)
            self.model = ct.model_class()
            initial=[]
            for num, field in zip(range(len(self.model._meta.fields)), self.model._meta.fields):
                if field.name != 'id':
                    initial.append({
                        'model_field':field.name,
                        'expression':'"%%s" %% csv_column[%s]' % str(num-1),
                        'enabled':True#(field.name != 'id' and True)
                        })
            self.initial = {1:initial}
        elif step == 1:
            remove_top = self.discard_firstrow and 0 or None
            self.mappings = form.cleaned_data
            #print 'mappings', dumps(self.mappings)
            results = perform_import(self.temp_file, self.model, self.mappings, remove_top=remove_top, dryrun=True)

            self.initial = {2:
                {'result_area':'\n'.join(results),
                'title':'Import dryrun results'}
            }
        elif step == 2:
            remove_top = self.discard_firstrow and 0 or None
            results = perform_import(self.temp_file, self.model, self.mappings, remove_top=remove_top, dryrun=True)
            self.initial = {3:
                {'result_area':'\n'.join(results),
                'title':'Final import results'}
            }
           
   
    def done(self, request, form_list):
        #TODO: delete self.temp_file
        return HttpResponseRedirect('/')
