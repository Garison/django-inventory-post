from django import forms 

#TODO: fix global import
from models import *

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('photos','active')


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('photos', 'inventory')

        
class RegionalOfficeForm(forms.ModelForm):
    class Meta:
        model = RegionalOffice


class ItemTemplateForm(forms.ModelForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos', 'supplies')


class ItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup

    
class LogForm(forms.ModelForm):
    class Meta:
        model = Log


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        exclude = ('photos')


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        
