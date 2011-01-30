from django import forms 
from django.utils.translation import ugettext_lazy as _

from generic_views.forms import DetailForm

from models import PurchaseRequest, PurchaseRequestItem, PurchaseOrder, \
                   PurchaseOrderItem
                   
#TODO: Remove auto_add_now from models and implement custom save method to include date              


class PurchaseRequestForm_view(DetailForm):
    class Meta:
        model = PurchaseRequest


class PurchaseRequestItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequestItem

    
class PurchaseOrderForm_view(DetailForm):
    class Meta:
        model = PurchaseOrder

    
class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
     

class PRIMakePOIForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #item_template = kwargs.pop('item_template', None)        
        super(PRIMakePOIForm, self).__init__(*args, **kwargs)
        if 'item_template' in self.initial:
        #    self.fields['template_id'].value = item_template.id
            self.fields['name'].initial = self.initial['item_template']
            self.fields['name'].show_hidden_initial = True
        #    #self.fields['suppliers'].choices = item_template.item_template.suppliers.all()
            #self.fields['suppliers'].choices = (('a','a'), ('b','b'))
            self.fields['suppliers'].choices = self.initial['item_template'].suppliers.all().values_list('id', 'name')

    #item = models.ForeignKey(
    template_id = forms.CharField()
    name = forms.CharField(label=_(u'Name'))
    suppliers = forms.ChoiceField()
    qty = forms.CharField()
#    model_field = forms.CharField(label=_(u'Model field'))
#    expression = forms.CharField(label=_(u'Expression'))
#    arguments = forms.CharField(label=_(u'Arguments'), required=False)
#    enabled = forms.BooleanField(label=_(u'Enabled'), required=False)
