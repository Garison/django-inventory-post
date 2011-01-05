from django import forms 

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

        
class FilterForm(forms.Form):
    def __init__(self, field_dict, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        for key in field_dict.keys():
            self.fields[key] = forms.ModelChoiceField(queryset=field_dict[key]['queryset'], required=False)
