from django import forms 
from django.utils.translation import ugettext_lazy as _

from generic_views.forms import DetailForm

from models import PurchaseRequest, PurchaseRequestItem, PurchaseOrder, \
                   PurchaseOrderItem
                   
#TODO: Remove auto_add_now from models and implement custom save method to include date              


class PurchaseRequestForm_view(DetailForm):
    def __init__(self, *args, **kwargs):
        super(PurchaseRequestForm_view, self).__init__(*args, **kwargs)    
        
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
     

class PurchaseOrderWizardItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PurchaseOrderWizardItemForm, self).__init__(*args, **kwargs)
        if 'item' in self.initial:
            self.fields['template_id'].initial = self.initial['item'].item_template.id
            self.fields['name'].initial = self.initial['item'].item_template
            self.fields['supplier'].choices = self.initial['item'].item_template.suppliers.all().values_list('id', 'name')
            self.fields['qty'].initial = self.initial['item'].qty

    template_id = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField(label=_(u'Name'))
    supplier = forms.ChoiceField(label=_(u'Suppliers'))
    qty = forms.CharField(label=_(u'Qty'))
