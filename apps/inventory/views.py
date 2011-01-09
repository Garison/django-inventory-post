from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.views.generic.list_detail import object_detail, object_list

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from photos.views import generic_photos

from generic_views.views import generic_assign_remove, generic_list

from models import Settings, Person, Item, ItemTemplate, \
                   ItemGroup, State, ItemState, Inventory, \
                   InventoryTransaction

from inventory import person_links, item_record_links, \
                      template_record_links, \
                      location_filter, navigation


def person_detail(request, object_id):
    return object_detail(
        request,
        queryset = Person.objects.all(),
        object_id = object_id,
        template_name = 'person_detail.html',
        extra_context={
            'record_links':person_links,
        },
    )


def person_assign_remove_item(request, object_id):
    person = get_object_or_404(Person, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign assets to the person: <a href="%s">%s</a>' % (person.get_absolute_url(), person)),
        obj=person,
        left_list_qryset=Item.objects.exclude(person=object_id), 
        right_list_qryset=person.inventory.all(), 
        add_method=person.inventory.add, 
        remove_method=person.inventory.remove, 
        left_list_title=_(u'Unassigned assets'), 
        right_list_title=_(u'Assigned assets'), 
        item_name=_(u"assets"), 
        list_filter=location_filter
    )


def template_assign_remove_supply(request, object_id):
    obj = get_object_or_404(ItemTemplate, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign supplies to the template: <a href="%s">%s</a>' % (obj.get_absolute_url(), obj)),        
        obj=obj,
        left_list_qryset=ItemTemplate.objects.exclude(supplies=obj).exclude(pk=obj.pk),
        right_list_qryset=obj.supplies.all(),
        add_method=obj.supplies.add,
        remove_method=obj.supplies.remove,
        left_list_title=_(u'Unassigned supplies'),
        right_list_title=_(u'Assigned supplies'),
        item_name=_(u"Supplies"))
            

def template_detail(request, object_id):
    return object_detail(
        request,
        queryset = ItemTemplate.objects.all(),
        object_id = object_id,
        template_name = 'itemtemplate_detail.html',
        extra_context={'record_links':template_record_links},
    )


def template_items(request, object_id):
    template = get_object_or_404(ItemTemplate, pk=object_id)
    return object_list(
        request,
        queryset = template.item_set.all(),
        template_name = "generic_list.html", 
        extra_context=dict(
            title = '%s: %s' % (_(u"assets that use the template"), template),
            create_view = 'item_create',
            record_links=item_record_links			
        ),
    )


def item_assign_remove_person(request, object_id):
    obj = get_object_or_404(Item, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign people to the asset: <a href="%s">%s</a>' % (obj.get_absolute_url(), obj)),                
        obj=obj,
        left_list_qryset=obj.get_nonowners(),
        right_list_qryset=obj.get_owners(),
        add_method=obj.add_owner,
        remove_method=obj.remove_owner,
        left_list_title=_(u"People that don't have this asset"),
        right_list_title=_(u"People that have this asset"),
        item_name=_(u"people"),
        list_filter=location_filter)

   
def item_detail(request, object_id, template_name=None, extra_data=None, passthru=False, show_create_view=True):
    if passthru:
        item = Item.objects_passthru.get(pk=object_id)
    else:
        item = get_object_or_404(Item, pk=object_id)

    extra_context={ 
        'template':item.item_template,
        'record_links':item_record_links,
        'title':_(u'the asset'),
        'subtitle':item,
        'item_photos_title':_(u'item photos'),
        'template_photos_title':_(u'template photos'),
        }


    if extra_data:
        for k, v in extra_data.iteritems():
            extra_context[k] = v

    if passthru:
        queryset = Item.objects_passthru.all()
    else:
        queryset = Item.objects.all()
        
    if not show_create_view:
        extra_context['item_create']=''
        
    if template_name:
        return object_detail(
            request,
            queryset = queryset,
            object_id = object_id,
            template_name = template_name,
            extra_context=extra_context,
        )
    else:
        return object_detail(
            request,
            queryset = queryset,
            object_id = object_id,
            extra_context=extra_context,
            template_name = 'item_detail.html'
        )

def item_setstate(request, object_id, state_id):
    item = get_object_or_404(Item, pk=object_id)
    state = get_object_or_404(State, pk=state_id)

    if state.id in ItemState.objects.states_for_item(item).values_list('state', flat=True):
        messages.error(request, _(u"This asset has already been marked as '%s'.") % state.name)
        return HttpResponseRedirect(reverse("item_view", args=[item.id]))    

    next = reverse("item_view", args=[item.id])
    data = {
        #'next':next,
        'object':item,
        'title':_(u"Are you sure you wish to mark this asset as '%s'?") % state.name,
    }    
    
    if state.exclusive:
        data['message'] = _(u"Any other states this asset may be marked as, will be cleared.")
   
    
    if request.method == 'POST':
        if state.exclusive:
            for item_state in ItemState.objects.states_for_item(item):
                item_state.delete()
        else:
            exclusive_state = ItemState.objects.states_for_item(item).filter(state__exclusive=True)
            if exclusive_state:
                messages.error(request, _(u"This asset has already been exclusively marked as '%s'.  Clear this state first.") % exclusive_state[0].state.name)
                return HttpResponseRedirect(reverse("item_view", args=[item.id]))                
            
                            
        new = ItemState(item=item, state=state)
        new.save()
            
        #item.active=False
        #item.save()		

        messages.success(request, _(u"The asset has been marked as '%s'.") % state.name)

        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', data,
    context_instance=RequestContext(request))       


def item_remove_state(request, object_id, state_id):
    item = get_object_or_404(Item, pk=object_id)
    state = get_object_or_404(State, pk=state_id)    
    next = reverse("item_view", args=[item.id])

    item_state = ItemState.objects.filter(item=item, state=state)
    if not item_state:
        messages.error(request, _(u"This asset is not marked as '%s'") % state.name)
        return HttpResponseRedirect(next)
        
    data = {
        #'next':next,
        'object':item,
        'title':_(u"Are you sure you wish to unmark this asset as '%s'?") % state.name,
    }       
    if request.method == 'POST':
        if item_state:
            try:
                item_state.delete()
                messages.success(request, _(u"The asset has been unmarked as '%s'.") % state.name)
            except:
                messages.error(request, _(u"Unable to unmark this asset as '%s'") % state.name)        
        
        return HttpResponseRedirect(next)
    
    return render_to_response('generic_confirm.html', data,
    context_instance=RequestContext(request))      


def item_state_list_init(request):
    try:
        state = State.objects.all()[0]
        return HttpResponseRedirect(reverse('item_state_list', args=[state.id]))
    except:
        messages.error(request, _(u"There are no asset states."))
        return HttpResponseRedirect(reverse('state_list'))
       
    
def item_state_list(request, state_id):
    item_state_menu_links = []
    
    for temp_state in State.objects.all():
        item_state_menu_links.append({
            'text':temp_state.name,
            'url':reverse(item_state_list, args=[temp_state.id]),
        })
    #TODO: HACKISH fix properly
    navigation[4]['links'] = item_state_menu_links

    state = get_object_or_404(State, pk=state_id)
    return generic_list(
        request,
        list_filter=location_filter, 
        queryset=Item.objects.filter(itemstate__state=state),
        extra_context={
            'title':_(u"assets marked as '%s'") % state.name,
            'create_view':'item_create',
            'record_links':item_record_links,
        }
    )
   

def group_assign_remove_item(request, object_id):
    obj = get_object_or_404(ItemGroup, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign assets to the group: <a href="%s">%s</a>' % (obj.get_absolute_url(), obj)),                
        obj=obj,
        left_list_qryset=Item.objects.exclude(itemgroup=obj),
        right_list_qryset=obj.items.all(),
        add_method=obj.items.add,
        remove_method=obj.items.remove,
        left_list_title=_(u"Unassigned assets"),
        right_list_title=_(u"Assigned assets"),
        item_name=_(u"assets"),
        list_filter=location_filter)

   
def inventory_current(request, object_id):
    inventory = get_object_or_404(Inventory, pk=object_id)
    transactions = InventoryTransaction.objects.filter(inventory=inventory)
    supply_qty={}
    for t in transactions:
        if t.supply in supply_qty:
            supply_qty[t.supply] = supply_qty[t.supply] + t.quantity
        else:
            supply_qty[t.supply] = t.quantity
        
    return render_to_response('inventory_current.html', {
        'inventory': inventory,
        'supply_qty': supply_qty,
    },
    context_instance=RequestContext(request))

def search(request):
    keyword=''
    people=None
    items=None
    templates=None
    groups=None
    
    if request.method == 'GET':
        keyword=request.GET.get('keyword','')
        
        if keyword:
            people = Person.objects.filter(
                Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(second_name__icontains=keyword) | Q(second_last_name__icontains=keyword ) | Q(location__name__icontains=keyword)
                )		

            items = Item.objects.filter(
                Q(property_number__icontains=keyword) | Q(notes__icontains=keyword) | Q(serial_number__icontains=keyword) | Q(location__name__icontains=keyword) | Q(item_template__description__icontains=keyword)
                )		

            templates = ItemTemplate.objects.filter(
                Q(description__icontains=keyword) | Q(brand__icontains=keyword) | Q(model__icontains=keyword) | Q(part_number__icontains=keyword) | Q(notes__icontains=keyword)
                )		

            groups = ItemGroup.objects.filter(
                Q(name__icontains=keyword)
                )	
         

    return render_to_response('search_results.html', {
        'people':people,
        'items':items,
        'templates':templates,
        'groups':groups,
        'keyword':keyword,
        },
    context_instance=RequestContext(request))

def item_log_list(request, object_id):
    item = Item.objects_passthru.get(pk=object_id)
    ctype = ContentType.objects.get_for_model(item)
    log=Log.objects.filter(content_type__pk=ctype.id, object_id=item.id)
    return object_list(
        request,
        queryset=log,
        template_name='generic_list.html',
        extra_context={'title':_(u"Asset log: %s") % item},
        ) 


'''
def render_to_pdf(template_src, context_dict):
    from django import http
    from django.shortcuts import render_to_response
    from django.template.loader import get_template
    from django.template import Context
    import ho.pisa as pisa
    import cStringIO as StringIO
    import cgi

    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

def report_items_per_person(request, object_id):
    person = Person.objects.get(pk=object_id)
    
    return render_to_pdf('report-items_per_person.html',
#	return render_to_response('report-items_per_person.html',
        {
            'pagesize':'A4',
            'object': person
        })
        
def fetch_resources(uri, rel):
    import os
    from django.conf import settings
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path
'''
