import os
import csv

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.simplejson import dumps, loads
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.formtools.wizard import FormWizard
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from api import perform_import
from wizard import BoundFormWizard

#TODO: Allow row 0 to be used as column names
#TODO: Load mapping in step 0 or reuse last import settings
#Ticket #7439 (new) FormWizard don't process multipart forms
#Ticket #11112 (new) Formsets not supported as steps in FormWizard   - DONE

def reduce_dict(d, l):
    return dict([(i, d[i]) for i in l])


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
            choices = sorted(["%s.%s" % (model.app_label, model.model) for model in qs])

        exclude = kwargs.pop('exclude', [])
        for exclusion in exclude:
            choices.remove(exclusion)

        super(DocumentForm, self).__init__(*args, **kwargs)
        
        capfirst = lambda x: x[0].upper() + x[1:]
        
        get_verbose_name = lambda x: getattr(x._meta, 'verbose_name', x) if hasattr(x, '_meta') else x
        
        names = [capfirst(get_verbose_name(ContentType.objects.get(app_label=model.split('.')[0], model=model.split('.')[1]).model_class())) for model in choices]
                
        self.fields['model_name'].choices=sorted(zip(choices, names), lambda x,y: 1 if x[1]>y[1] else -1)
        
    local_document = DocumentField(label=_(u'Local document'))
    model_name = forms.ChoiceField(label=_(u'Model'), help_text=_(u'Model that will receive the data.'))
    #import_mappings = forms.FileField(label=_(u'Import mappings file (optional)'), required=False)



class PreviewForm(forms.Form):
    preview_area = forms.CharField(label=_(u'Preview'), required=False, widget=forms.widgets.Textarea(attrs={'cols':80, 'rows':10}))
    start_row = forms.IntegerField(label=_(u'Start row'), initial=1)
    dialect_delimiter = forms.CharField(label=_('Delimiter'), max_length=1, help_text=_(u'A one-character string used to separate fields. It defaults to ",".'))
    dialect_quotechar = forms.CharField(label=_('Quote character'), max_length=1, help_text=_(u'A one-character string used to quote fields containing special characters, such as the delimiter or quote character, or which contain new-line characters. It defaults to ".'))
    dialect_doublequote = forms.BooleanField(label=_('Doublequote'), required=False, help_text=_(u'Controls how instances of the quote character appearing inside a field should be themselves be quoted. When True, the character is doubled. When False, the escape character is used as a prefix to the quote character. It defaults to True.'))
    dialect_escapechar = forms.CharField(label=_('Escape character'), max_length=1, required=False, help_text=_(u'The escape character removes any special meaning from the following character. It defaults to None, which disables escaping.'))
    dialect_skipinitialspace = forms.BooleanField(label=_('Skip initial space'), required=False, help_text=_(u'When True, whitespace immediately following the delimiter is ignored. The default is False.'))


class ExpressionForm(forms.Form):
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
    

class ImportWizard(BoundFormWizard):
    def store_settings(self, request, settings_list):
        request.session['last_import_settings'] = reduce_dict(self.settings, settings_list)

    def sniff_file(self):
        csvfile = open(self.settings['filename'], 'rb')
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        self.initial = {0:{
                'preview_area':''.join([csvfile.readline() for i in range(10)]),
                'dialect_delimiter':dialect.delimiter,
                'dialect_doublequote':dialect.doublequote,
                'dialect_escapechar':dialect.escapechar,
                'dialect_quotechar':dialect.quotechar,
                'dialect_skipinitialspace':dialect.skipinitialspace,
            }}
        csvfile.close()

    def render_template(self, request, form, previous_fields, step, context=None):
        context = {'step_title':self.extra_context['step_titles'][step]}
        return super(ImportWizard, self).render_template(request, form, previous_fields, step, context)
       
    def parse_params(self, request, *args, **kwargs):
        self.extra_context={'step_titles':[
            _(u'step 1 of 4: Import preview'),
            _(u'step 2 of 4: expressions'),
            _(u'step 3 of 4: Import test run results'),
            _(u'step 4 of 4: Final import results'),
            ]}
        self.settings = {}
        self.settings['filename'] = request.GET.get('temp_file', None)
        self.settings['model_name'] = request.GET.get('model_name', None)
        if not self.settings['filename']:
            raise Http404
            
        try:
            self.sniff_file()
        except IOError, err:
            raise Http404(err)
        
    def get_template(self, step):
        return 'import_wizard.html'
    
       
    def process_step(self, request, form, step):
        if step == 0:
            self.settings['dialect_settings'] = dict([(key, form.cleaned_data[key]) for key in form.cleaned_data if 'dialect' in key])
            self.settings['start_row'] = form.cleaned_data['start_row']
            #app_label, name = self.settings['model_name'].split('.')
            app_label, model = self.settings['model_name'].split('.')
            #ct = ContentType.objects.get(app_label=app_label, name=name)
            ct = ContentType.objects.get(app_label=app_label, model=model)
            self.settings['model'] = ct.model_class()
            initial=[]
            for num, field in enumerate(self.settings['model']._meta.fields):
                if field.name != 'id':
                    initial.append({
                        'model_field':field.name,
                        'expression':'"%%s" %% csv_column[%s]' % str(num-1),
                        'enabled':field.name != 'id' and True
                        })
            self.initial = {1:initial}
        elif step == 1:
            self.settings['expressions'] = form.cleaned_data
            results = perform_import(self.settings['filename'], self.settings['model'], self.settings['expressions'], dialect_settings=self.settings['dialect_settings'], start_row=self.settings['start_row'], dryrun=True)

            self.initial = {2:
                {'result_area':'\n'.join(results),
                'title':_(u'Import test run results')}
            }
        elif step == 2:
            self.store_settings(request, ['model_name', 'start_row', 'expressions', 'dialect_settings'])
            results = perform_import(self.settings['filename'], self.settings['model'], self.settings['expressions'], dialect_settings=self.settings['dialect_settings'], start_row=self.settings['start_row'], dryrun=False)
            
            self.initial = {3:
                {'result_area':'\n'.join(results),
                'title':_(u'Final import results')}
            }
           
   
    def done(self, request, form_list):
        os.unlink(self.settings['filename'])
        return HttpResponseRedirect('/')
