from django import forms 
from django.utils.translation import ugettext_lazy as _


from generic_views.forms import DetailForm

from models import Item, Person, ItemGroup



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

        
class ItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        exclude = ('items',)

class ItemGroupForm_view(DetailForm):
    class Meta:
        model = ItemGroup
