from django import forms 
from django.utils.translation import ugettext_lazy as _


from generic_views.forms import DetailForm

from models import ItemTemplate, Log, \
                   InventoryTransaction, Inventory, Supplier, Location


class LocationForm_view(DetailForm):
    class Meta:
        model = Location
       
      
class ItemTemplateForm(forms.ModelForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos', 'supplies', 'suppliers')


class ItemTemplateForm_view(DetailForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos',)

    
class LogForm(forms.ModelForm):
    class Meta:
        model = Log


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        
        
class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=128, label=_(u'Search term'))
    
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
