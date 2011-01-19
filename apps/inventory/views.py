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

from models import Settings, ItemTemplate, Inventory, \
                   InventoryTransaction, Supplier

from inventory import template_record_links, \
                      location_filter, navigation

from forms import SearchForm


def supplier_assign_remove_itemtemplates(request, object_id):
    obj = get_object_or_404(Supplier, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign templates to the supplier: <a href="%(url)s">%(obj)s</a>' % {'url':obj.get_absolute_url(), 'obj':obj}),
        obj=obj,
        left_list_qryset=ItemTemplate.objects.exclude(suppliers=obj), 
        right_list_qryset=obj.itemtemplate_set.all(), 
        add_method=obj.itemtemplate_set.add, 
        remove_method=obj.itemtemplate_set.remove, 
        left_list_title=_(u'Unassigned templates'), 
        right_list_title=_(u'Assigned templates'), 
        item_name=_(u"templates"), 
    )
    
def template_assign_remove_supply(request, object_id):
    obj = get_object_or_404(ItemTemplate, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign supplies to the template: <a href="%(url)s">%(obj)s</a>' % {'url':obj.get_absolute_url(), 'obj':obj}),        
        obj=obj,
        left_list_qryset=ItemTemplate.objects.exclude(supplies=obj).exclude(pk=obj.pk),
        right_list_qryset=obj.supplies.all(),
        add_method=obj.supplies.add,
        remove_method=obj.supplies.remove,
        left_list_title=_(u'Unassigned supplies'),
        right_list_title=_(u'Assigned supplies'),
        item_name=_(u"supplies"))
           

def template_assign_remove_suppliers(request, object_id):
    obj = get_object_or_404(ItemTemplate, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign suppliers to the template: <a href="%(url)s">%(obj)s</a>' % {'url':obj.get_absolute_url(), 'obj':obj}),        
        obj=obj,
        left_list_qryset=Supplier.objects.exclude(itemtemplate=obj),
        right_list_qryset=obj.suppliers.all(),
        add_method=obj.suppliers.add,
        remove_method=obj.suppliers.remove,
        left_list_title=_(u'Unassigned suppliers'),
        right_list_title=_(u'Assigned suppliers'),
        item_name=_(u"suppliers"))
            

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
    keyword = ''
    people = None
    items = None
    templates = None
    groups = None
    form = SearchForm()
    
    if request.method == 'GET':
        keyword=request.GET.get('keyword','')
        form = SearchForm(initial={'keyword':keyword})        
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
        'form':form,
        'people':people,
        'items':items,
        'templates':templates,
        'groups':groups,
        'keyword':keyword,
        },
    context_instance=RequestContext(request))

'''
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
