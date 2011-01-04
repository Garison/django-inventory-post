from django import forms 

#TODO: fix global import
from models import *

#TODO: maybe dynamic generation from view is better?
#Generic forms for generic views
class GenericConfirmForm(forms.Form):
    pass


class GenericAssignRemoveForm(forms.Form):
    left_list = forms.ModelMultipleChoiceField(required=False, queryset=None)
    right_list = forms.ModelMultipleChoiceField(required=False, queryset=None)
    def __init__(self, left_list_qryset, right_list_qryset, left_filter=None, *args, **kwargs):
        super(GenericAssignRemoveForm, self).__init__(*args, **kwargs)
        if left_filter:
            self.fields['left_list'].queryset = left_list_qryset.filter(*left_filter)
        else:
            self.fields['left_list'].queryset = left_list_qryset

        self.fields['right_list'].queryset = right_list_qryset


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

        
class FilterForm(forms.Form):
    def __init__(self, field_dict, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        for key in field_dict.keys():
            self.fields[key] = forms.ModelChoiceField(queryset=field_dict[key]['queryset'], required=False)


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
        
