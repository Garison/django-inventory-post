from django import forms 
from django.utils.translation import ugettext_lazy as _


from generic_views.forms import DetailForm

from models import Item, Person, ItemTemplate, ItemGroup, Log, \
                   InventoryTransaction, Inventory, Supplier


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('photos', 'active')


class ItemForm_view(DetailForm):
    class Meta:
        model = Item
        exclude = ('photos', 'active')


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('photos', 'inventory')


class PersonForm_view(DetailForm):
    class Meta:
        model = Person
        exclude = ('photos',)

        
class ItemTemplateForm(forms.ModelForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos', 'supplies', 'suppliers')


class ItemTemplateForm_view(DetailForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos',)


class ItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        exclude = ('items',)

    
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
