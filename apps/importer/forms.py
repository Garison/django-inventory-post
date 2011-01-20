import os
import csv

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect


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
        super(DocumentForm, self).__init__(*args, **kwargs)

        models = kwargs.pop('models', [])
        if models:
            choices = models
        else:
            qs=ContentType.objects.all()
            choices = sorted(["%s.%s" % (model.app_label, model.name) for model in qs])

        exclude = kwargs.pop('exclude', [])
        for exclusion in exclude:
            choices.remove(exclusion)
            
        self.fields['model_name'].choices=zip(choices, choices)
        
    local_document = DocumentField(label=_(u'Local document'))
    model_name = forms.ChoiceField(label=_(u'Model'), help_text=_(u'Model that will receive the data.'))
    #import_mappings = forms.FileField(label=_(u'Import mappings file (optional)'), required=False)


class PreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #print 'PreviewForm', args, kwargs
        self.title = _(u'import preview')
        super(PreviewForm, self).__init__(*args, **kwargs)
            
    preview_area = forms.CharField(label=_(u'Preview'), required=False, widget=forms.widgets.Textarea(attrs={'cols':80, 'rows':10}))
    discard_firstrow = forms.BooleanField(label=_(u'Discard first row'), required=False)


class ExpressionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExpressionForm, self).__init__(*args, **kwargs)

    model_field = forms.CharField(label=_(u'Model field'))
    expression = forms.CharField(label=_(u'Expression'))
    enabled = forms.BooleanField(label=_(u'Enabled'), required=False)


class ImportResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.title = _(u'import results')
        super(ImportResultForm, self).__init__(*args, **kwargs)
        
    result_area = forms.CharField(label=_(u'Results'), required=False, widget=forms.widgets.Textarea(attrs={'cols':80, 'rows':10}))
    

class ImportWizard(FormWizard):
    def parse_params(self, request, *args, **kwargs):
        self.temp_file = request.GET.get('temp_file', None)
        self.model_name = request.GET.get('model_name', None)

        csvfile = open(self.temp_file, 'rb')
        #dialect = csv.Sniffer().sniff(csvfile.read(1024))
        #print 'delimiter', dialect.delimiter
        #print 'doublequote', dialect.doublequote
        #print 'escapechar', dialect.escapechar
        #print 'lineterminator', dialect.lineterminator
        #print 'quotechar', dialect.quotechar
        #print 'quoting', dialect.quoting
        #csvfile.seek(0)

        self.initial = {0:
            {'preview_area':''.join([csvfile.readline() for i in range(10)])}
        }
        
    def get_template(self, step):
        return 'import_wizard.html'
        
#    def render_template(self, request, form, previous_fields, step, context=None):
        #context={'title':'asdf'}
        #if step == 0:
#            self.temp_file = request.GET.get('temp_file', None)
#            self.mode_name = request.GET.get('mode_name', None)
#        return super(ImportWizard, self).render_template(request, form, previous_fields, step, context)
    def render(self, form, request, step, context=None):
        "Renders the given Form object, returning an HttpResponse."
        old_data = request.POST
        prev_fields = []
        if old_data:
            hidden = forms.HiddenInput()
            # Collect all data from previous steps and render it as HTML hidden fields.
            for i in range(step):
                old_form = self.get_form(i, old_data)
                hash_name = 'hash_%s' % i
                if hasattr(old_form, 'management_form'):
                    for form_in_set in old_form.forms:
                        prev_fields.extend([bf.as_hidden() for bf in form_in_set])
                        prev_fields.append(hidden.render(hash_name, old_data.get(hash_name, self.security_hash(request, form_in_set))))
                else:
                    prev_fields.extend([bf.as_hidden() for bf in old_form])
                    prev_fields.append(hidden.render(hash_name, old_data.get(hash_name, self.security_hash(request, old_form))))
        return self.render_template(request, form, ''.join(prev_fields), step, context)


    def get_form(self, step, data=None):
        initial=self.initial.get(step, None)
        if hasattr(self.form_list[step], 'management_form'):
            initial=self.initial.get(step, None)
            if initial:
                initial = initial['initial']

        return self.form_list[step](data, prefix=self.prefix_for_step(step), initial=initial)

        
    def process_step(self, request, form, step):
        if step == 0:
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
            self.initial = {1:
                {'initial':initial}
            }
        elif step == 1:
            csvfile = open(self.temp_file, 'rb')
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            
            #reader = csv.reader(open(self.temp_file, 'r'), dialect=dialect)

            try:
                csvfile = file(self.temp_file, 'r')
            except IOError:
                self.error('Could not open specified csv file, %s, or it does not exist' % datafile, 0)
            else:
                # CSV Reader returns an iterable, but as we possibly need to
                # perform list commands and since list is an acceptable iterable, 
                # we'll just transform it.
                csvfile = list(csv.reader(csvfile, dialect=dialect))

            #model_fields = dict([(f.name,f) for f in self.model._meta.fields])
            model_fields = self.model._meta.init_name_map()
            for line, column in zip(range(len(csvfile)), csvfile):
                model_line = {}
                print 'line', line
                for field_exp in form.cleaned_data:
                    if field_exp['enabled']:
                        #if model._meta.
                        field = model_fields[field_exp['model_field']][0]
                        print field
                        if hasattr(field, 'related'):
                            value = field.related.parent_model.objects.get(description='Dell')
                            value = 9
                        else:
                            value = eval(field_exp['expression'], {'csv_column':column})
                            print 'value', value
                            
                        #related.parent_model
                        model_line[field_exp['model_field']] = value
                    #print value
                    #except:
                
                #print model_line
                try:
                    entry = self.model(**model_line)
                except Exception, err:
                    print 'Import error, line: %s, error: %s' % (line, err)
                
                #print 'entry', entry
                #print entry.full_clean()
        #elif step == 2:
        #    self.initial = {2:
        #        {'result_area':'as'}
        #    }            
            
            
        #print 'process_step', step
   
    def done(self, request, form_list):
        return HttpResponseRedirect('/')
