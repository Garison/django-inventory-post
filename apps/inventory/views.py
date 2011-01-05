from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.views.generic.list_detail import object_detail, object_list

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from photos.views import generic_photos

from generic_views.views import generic_assign_remove

from models import Settings, Person, Item, ItemTemplate, Supply

from inventory import person_links, item_record_links, \
                      template_record_links, retireditem_links, \
                      supply_record_links, inrepairsitem_links, \
                      location_filter


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

    
def item_detail(request, object_id, template_name=None, extra_data=None, passthru=False, show_create_view=True):
    if passthru:
        item = Item.objects_passthru.get(pk=object_id)
    else:
        item = get_object_or_404(Item, pk=object_id)

    extra_context={ 
        'photos':item.photos.all(),
        'template_photos':item.item_template.photos.all(),
        'template':item.item_template,
        'record_links':item_record_links,
        'title':_(u'the asset'),
        'subtitle':item,
        'item_photos_title':_(u'item photos'),
        'template_photos_title':_(u'template photos'),
        }

    in_repairs = item.is_inrepairs()
    if in_repairs:
        extra_context['extra_attribs'] = {
            _(u'In repairs since'):in_repairs.date,
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


def person_detail(request, object_id):
    return object_detail(
        request,
        queryset = Person.objects.all(),
        object_id = object_id,
        template_name = 'person_detail.html',
        extra_context={'photos':get_object_or_404(Person, pk=object_id).photos.all(), 'record_links':person_links},
    )

def person_assign_remove_item(request, object_id):
    person = get_object_or_404(Person, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u"asset to user"), 
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

def supply_assign_remove_template(request, object_id):
    supply = get_object_or_404(Supply, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u"supplies to template"),
        obj=supply,
        left_list_qryset=supply.get_nonowners(),
        right_list_qryset=supply.get_owners(),
        add_method=supply.add_owner,
        remove_method=supply.remove_owner,
        left_list_title=_(u'Unassigned templates'),
        right_list_title=_(u'Assigned templates'),
        item_name=_(u"templates"))     

def template_assign_remove_supply(request, object_id):
    obj = get_object_or_404(ItemTemplate, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u"template supplies"),
        obj=obj,
        left_list_qryset=Supply.objects.exclude(itemtemplate=obj),
        right_list_qryset=obj.supplies.all(),
        add_method=obj.supplies.add,
        remove_method=obj.supplies.remove,
        left_list_title=_(u'Unassigned supplies'),
        right_list_title=_(u'Assigned supplies'),
        item_name=_(u"Supplies"))
        
        
def item_assign_remove_person(request, object_id):
    obj = get_object_or_404(Item, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u"to users of the asset"),
        obj=obj,
        left_list_qryset=obj.get_nonowners(),
        right_list_qryset=obj.get_owners(),
        add_method=obj.add_owner,
        remove_method=obj.remove_owner,
        left_list_title=_(u"Users that don't have this asset"),
        right_list_title=_(u"Users that have this asset"),
        item_name=_(u"users"),
        list_filter=location_filter)

def template_detail(request, object_id):
    return object_detail(
        request,
        queryset = ItemTemplate.objects.all(),
        object_id = object_id,
        template_name = 'itemtemplate_detail.html',
        extra_context={'photos':get_object_or_404(ItemTemplate, pk=object_id).photos.all(), 'record_links':template_record_links},
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


def supply_detail(request, object_id):
    return object_detail(
        request,
        queryset=Supply.objects.all(),
        object_id=object_id,
        template_name='supply_detail.html',
        extra_context={'photos':get_object_or_404(Supply, pk=object_id).photos.all(), 'record_links':supply_record_links},
    )


def supply_templates(request, object_id):
    supply = get_object_or_404(Supply, pk=object_id)
    return object_list(
        request,
        queryset = supply.itemtemplate_set.all(),
        template_name = "generic_list.html", 
        extra_context=dict(
            title = '%s: %s' % (_(u"templates that use the supply"), supply),
            create_view = 'item_create',
            record_links=template_record_links			
        ),
    )



def search(request):
    keyword=''
    people=None
    items=None
    templates=None
    groups=None
    supplies=None
    
    if request.method == 'GET':
        keyword=request.GET.get('keyword','')
        
        if keyword:
            people = Person.objects.filter(
                Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(second_name__icontains=keyword) | Q(second_last_name__icontains=keyword ) | Q(regional_office__name__icontains=keyword) | Q(photos__title__icontains=keyword )
                )		

            items = Item.objects.filter(
                Q(property_number__icontains=keyword) | Q(notes__icontains=keyword) | Q(serial_number__icontains=keyword) | Q(photos__title__icontains=keyword ) | Q(regional_office__name__icontains=keyword) | Q(department__name__icontains=keyword) | Q(item_template__description__icontains=keyword)
                )		

            templates = ItemTemplate.objects.filter(
                Q(description__icontains=keyword) | Q(brand__icontains=keyword) | Q(model__icontains=keyword) | Q(photos__title__icontains=keyword ) | Q(part_number__icontains=keyword) | Q(notes__icontains=keyword)
                )		

            supplies = Supply.objects.filter(
                Q(description__icontains=keyword) | Q(brand__icontains=keyword) | Q(model__icontains=keyword) | Q(photos__title__icontains=keyword ) | Q(part_number__icontains=keyword) | Q(notes__icontains=keyword) | Q(itemtemplate__description__icontains=keyword) | Q(itemtemplate__brand__icontains=keyword) | Q(itemtemplate__model__icontains=keyword) | Q(itemtemplate__photos__title__icontains=keyword ) | Q(itemtemplate__part_number__icontains=keyword) | Q(itemtemplate__notes__icontains=keyword)
                )		

            groups = ItemGroup.objects.filter(
                Q(name__icontains=keyword)
                )	

            retired_items = RetiredItem.objects.filter(
                Q(item__property_number__icontains=keyword) | Q(item__notes__icontains=keyword) | Q(item__serial_number__icontains=keyword) | Q(item__photos__title__icontains=keyword ) | Q(item__regional_office__name__icontains=keyword) | Q(item__department__name__icontains=keyword) | Q(item__item_template__description__icontains=keyword) | Q(item__item_template__brand__icontains=keyword) | Q(item__item_template__model__icontains=keyword) | Q(item__item_template__photos__title__icontains=keyword ) | Q(item__item_template__part_number__icontains=keyword) | Q(item__item_template__notes__icontains=keyword)
                )		
                
#			results = []
#			for i in people:
#				results.append(i)
#
#			for i in items:
#				results.append(i)
#
#			for i in templates:
#				results.append(i)
#
#			for i in groups:
#				results.append(i)

    return render_to_response('search_results.html', {
        'people':people,
        'items':items,
        'templates':templates,
        'groups':groups,
        'retired_items':retired_items,
        'keyword':keyword,
        'supplies':supplies,
#		'results': results,
        },
    context_instance=RequestContext(request))


def retireditem_detail(request, object_id):
    retired_item = get_object_or_404(RetiredItem, pk=object_id)
    extra_data={ 
        'wrapper_object':retired_item,
        'record_links':retireditem_links,	
        'title':_(u"retired asset"),
        'subtitle':retired_item.item,
        'extra_attribs':{
                _(u'Retired'):retired_item.date
                }
         }
    
    return item_detail(request, retired_item.item_id, template_name='item_detail.html', extra_data=extra_data, passthru=True)


def item_retire(request, object_id):
    item = Item.objects.get(pk=object_id)

    new = RetiredItem(item=item)
    new.save()

    for owner in item.get_owners():
        owner.inventory.remove(item)

    try: 
        inrepairs = InRepairsItem.objects.get(item=item)
        inrepairs.delete()
    except:
        pass

    item.active=False
    item.save()		

    messages.success(request, _(u"The asset has been marked as retired."))

    return HttpResponseRedirect(reverse('retireditem_list'))
    

def retireditem_unretire(request, object_id):
    retired_item = RetiredItem.objects.get(pk=object_id)

    item = Item.objects_passthru.filter(pk=retired_item.item.id)
    item.update(active=True)
#HACK: because of custom manager .save() doesn;t see the item and tries to create new record

    retired_item.delete()
    return HttpResponseRedirect(reverse('retireditem_list'))

def inrepairsitem_detail(request, object_id):
    inrepairs_item = get_object_or_404(InRepairsItem, pk=object_id)
    extra_data={ 
        'wrapper_object' : inrepairs_item,
        'record_links' : inrepairsitem_links,
        'title' : _(u"asset in repairs"),
        'extra_attribs' : {
            _(u'In repairs since') : inrepairs_item.date,
            }
         }
    
    return item_detail(request, inrepairs_item.item_id, template_name='item_detail.html', extra_data=extra_data, show_create_view=False)


def item_sendtorepairs(request, object_id):
    item = Item.objects.get(pk=object_id)
    if InRepairsItem.objects.filter(item=item):
        messages.warning(request, _(u"This asset is in repairs."))

        return HttpResponseRedirect(reverse('inrepairsitem_list'))			

    new = InRepairsItem(item=item)
    new.save()

    messages.success(request, _(u"The asset has been marked as 'in repairs'."))

    return HttpResponseRedirect(reverse('inrepairsitem_list'))


def inrepairsitem_unrepair(request, object_id):
    try:
        inrepairs = InRepairsItem.objects.get(pk=object_id)
        inrepairs.delete()
    except:
        messages.warning(request, _(u"This asset is not in repairs."))
    
    return HttpResponseRedirect(reverse('inrepairsitem_list'))			

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
'''
        
restricted_views = ['generic_photos', 'generic_update', 'generic_create', 'generic_delete', 'generic_confirm']
if Settings.objects.get(pk=1).is_anon_restricted:
    restricted_views += ['generic_list', 'generic_detail', 'item_detail', 'person_detail', 'template_detail']

for view in restricted_views:
    exec ("%s=login_required(%s)" % (view, view))
'''
