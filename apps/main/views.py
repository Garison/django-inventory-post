from django.shortcuts import render_to_response
from django.template import RequestContext

from inventory.models import Person, Item, ItemTemplate


def home(request):
    data =  {
        'person':Person.objects.all(),
        'item':Item.objects.all(),
        'template':ItemTemplate.objects.all(),
    }

    return render_to_response('home.html', data,
    context_instance=RequestContext(request))     
