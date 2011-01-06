from django.template.defaultfilters import stringfilter
from django.template import Library, Node, Variable
from django.core.urlresolvers import reverse

from photos.models import GenericPhoto 

register = Library()

@register.filter
#@stringfilter
def get_photos_for_object(value):
    return GenericPhoto.objects.photos_for_object(value)
