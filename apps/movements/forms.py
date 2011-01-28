from django import forms 
from django.utils.translation import ugettext_lazy as _

from generic_views.forms import DetailForm

from models import PurchaseRequest, PurchaseRequestItem


class PurchaseRequestForm_view(DetailForm):
    class Meta:
        model = PurchaseRequest

class PurchaseRequestItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequestItem
    
