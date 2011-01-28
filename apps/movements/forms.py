from django import forms 
from django.utils.translation import ugettext_lazy as _

from generic_views.forms import DetailForm

from models import PurchaseRequest, PurchaseRequestItem, PurchaseOrder, \
                   PurchaseOrderItem
                   
#TODO: Remove auto_add_now from models and implement custom save method to include data                   


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
    
