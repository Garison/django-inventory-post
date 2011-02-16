from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse

from generic_views.views import generic_assign_remove, generic_list

from photos.views import generic_photos

from assets.models import Person, Item, ItemGroup

from models import ItemTemplate, Inventory, \
                   InventoryTransaction, Supplier

from inventory import location_filter

from forms import InventoryForm_view, InventoryTransactionForm


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
        ),
    )

def inventory_view(request, object_id):
    inventory = get_object_or_404(Inventory, pk=object_id)
    form = InventoryForm_view(instance=inventory)
    
    return render_to_response('generic_detail.html', {
        'object_name':_(u'inventory'),
        'object':inventory,
        'form':form,
        'subtemplates_dict':[{
            'name':'generic_list_subtemplate.html',
            'title':_(u'inventory transactions'),
            'object_list':inventory.inventorytransaction_set.all(),
            'hide_object':True,

            'extra_columns':[
                {'name':_(u'date'), 'attribute':'date'},
                {'name':_(u'item'), 'attribute':'supply'},
                {'name':_(u'qty'), 'attribute':'quantity'},
            ],
        }]
    },
    context_instance=RequestContext(request))


def inventory_create_transaction(request, object_id):
    inventory = get_object_or_404(Inventory, pk=object_id)
    
    if request.method == 'POST':
        form = InventoryTransactionForm(request.POST)#, initial={'purchase_order':purchase_order})
        if form.is_valid():
            form.save()
            msg = _(u'The inventory transaction was created successfully.')
            messages.success(request, msg, fail_silently=True)            
            return redirect(inventory.get_absolute_url())
    else:
        form = InventoryTransactionForm(initial={'inventory':inventory})

    return render_to_response('generic_form.html', {
        'form':form,
        'object':inventory,
        'title':_(u'add new transaction') ,
    },
    context_instance=RequestContext(request))

def inventory_current(request, object_id):
    inventory = get_object_or_404(Inventory, pk=object_id)
    transactions = InventoryTransaction.objects.filter(inventory=inventory)
    supply_qty={}
    for t in transactions:
        if t.supply in supply_qty:
            supply_qty[t.supply] = supply_qty[t.supply] + t.quantity
        else:
            supply_qty[t.supply] = t.quantity
    
    supplies_list = [{'item_template':x, 'qty':y} for x,y in supply_qty.items()]
    return render_to_response('generic_list.html', {
        'object_list':supplies_list,
        'extra_columns':[{'name':_(u'quantity'),'attribute':'qty'}],
        'main_object':'item_template',
        'object':inventory,
        'title':_(u'current balances for inventory: %s') % inventory,
    },
    context_instance=RequestContext(request))


def supplier_purchase_orders(request, object_id):
    supplier = get_object_or_404(Supplier, pk=object_id)
    return object_list(
        request,
        queryset = supplier.purchaseorder_set.all(),
        template_name = "generic_list.html", 
        extra_context=dict(
            title = '%s: %s' % (_(u"purchase orders from supplier"), supplier),
        ),
    )


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
