from django import forms 

from models import Item, Person, ItemTemplate, ItemGroup, Log, Permission, \
                   InventoryTransaction, Inventory

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('photos', 'active')


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('photos', 'inventory')

        
class ItemTemplateForm(forms.ModelForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos', 'supplies')


class ItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        exclude = ('items',)

    
class LogForm(forms.ModelForm):
    class Meta:
        model = Log


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        
