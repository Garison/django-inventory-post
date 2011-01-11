from django import forms 
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class DetailSelectMultiple(forms.widgets.SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = u''
        options = [string for index, string in self.choices if index in value]
        if options:
            output += ', '.join(options)
        else:
            output = _(u"None")
        return mark_safe(output + u'\n')
         

class DetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.SelectMultiple):
                self.fields[field_name].widget = DetailSelectMultiple(
                    choices=field.widget.choices,
                    attrs=field.widget.attrs,
                )
                self.fields[field_name].help_text=''


class GenericConfirmForm(forms.Form):
    pass


class GenericAssignRemoveForm(forms.Form):
    left_list = forms.ModelMultipleChoiceField(required=False, queryset=None)
    right_list = forms.ModelMultipleChoiceField(required=False, queryset=None)
    def __init__(self, left_list_qryset=None, right_list_qryset=None, left_filter=None, *args, **kwargs):
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
