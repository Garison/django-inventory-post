import os

from django import forms
from django.utils.translation import ugettext_lazy as _
#from django.http import HttpResponseRedirect
#from django.contrib.formtools.wizard import FormWizard
from django.contrib.contenttypes.models import ContentType


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
    local_document = DocumentField(label=_(u'Local document'))
    selected_model = forms.ChoiceField(label=_(u'Model'), help_text=_(u'Model that will receive the data.'), choices=[(model.name,model.name) for model in ContentType.objects.all()])


class DialectForm(forms.Form):
    preview_area = forms.CharField(label=_(u'Preview'), required=False, widget=forms.widgets.Textarea(attrs={'cols':80, 'rows':10}))
    discard_firstrow = forms.BooleanField(label=_(u'Discard first row'))


class ImportExpression(forms.Form):
    expression = forms.CharField(label=_(u'Expression'))
    enabled = forms.BooleanField(label=_(u'Enabled'))

'''
class ImportWizard(FormWizard):
    def get_template(self, step):
        return 'import_wizard.html'
        
    def process_step(self, request, form, step):
        print form.is_multipart
   
    def done(self, request, form_list):
        return HttpResponseRedirect('/')
'''
