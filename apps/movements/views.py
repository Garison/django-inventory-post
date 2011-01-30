from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object


from models import PurchaseRequest, PurchaseRequestItem, PurchaseOrder
from forms import PurchaseRequestForm_view, PurchaseRequestItemForm, \
                  PurchaseOrderForm_view, PurchaseOrderItemForm, \
                  PurchaseOrderItem
                  
def purchase_request_view(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)
    form = PurchaseRequestForm_view(instance=purchase_request)
    
    return render_to_response('generic_detail.html', {
        'title':_(u'details for purchase request: %s') % purchase_request,
        'object':purchase_request,
        'form':form,
        'subtemplates_dict':[{
            'name':'generic_list_subtemplate.html',
            'title':_(u'purchase request items'),
            'object_list':purchase_request.purchaserequestitem_set.all(),
            'extra_columns':[{'name':_(u'qty'), 'attribute':'qty'}],
        }]
    },
    context_instance=RequestContext(request))


def purchase_request_item_create(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)
    
    if request.method == 'POST':
        form = PurchaseRequestItemForm(request.POST)#, initial={'purchase_request':purchase_request})
        if form.is_valid():
            form.save()
            msg = _(u'The purchase request item was created successfully.')
            messages.success(request, msg, fail_silently=True)            
            return redirect(purchase_request.get_absolute_url())
    else:
        form = PurchaseRequestItemForm(initial={'purchase_request':purchase_request})

    return render_to_response('generic_form.html', {
        'form':form,
        'title':_(u'add new purchase request item') ,
    },
    context_instance=RequestContext(request))
    
    #form = PurchaseRequestItemForm#(purchase_request=purchase_request)
    
    #return create_object(request, 
    #    #model=PurchaseRequestItem#,(purchase_request=purchase_request),
    #    form_class=form,
    #    template_name='generic_form.html',
    #    extra_context={'object':purchase_request},
    #) 
    
def purchase_request_close(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)    

    data = {
        'object':purchase_request,
        'title':_(u"Are you sure you wish to close the purchase request: %s?") % purchase_request,
    }
        
    if purchase_request.active == False:
        msg = _(u'This purchase request has already been closed.')
        messages.error(request, msg, fail_silently=True)            
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_request.get_absolute_url())
        
    if request.method == 'POST':
        purchase_request.active = False
        purchase_request.save()
        msg = _(u'The purchase request has been closed successfully.')
        messages.success(request, msg, fail_silently=True)            
        return redirect(purchase_request.get_absolute_url())

    return render_to_response('generic_confirm.html', data,
    context_instance=RequestContext(request))  
    
    
def purchase_request_open(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)    

    data = {
        'object':purchase_request,
        'title':_(u"Are you sure you wish to open the purchase request: %s?") % purchase_request,
    }
        
    if purchase_request.active == True:
        msg = _(u'This purchase request is already open.')
        messages.error(request, msg, fail_silently=True)            
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_request.get_absolute_url())
        
    if request.method == 'POST':
        purchase_request.active = True
        purchase_request.save()
        msg = _(u'The purchase request has been opened successfully.')
        messages.success(request, msg, fail_silently=True)            
        return redirect(purchase_request.get_absolute_url())

    return render_to_response('generic_confirm.html', data,
    context_instance=RequestContext(request))  


from forms import PRIMakePOIForm
from django.forms.formsets import formset_factory

def purchase_request_make_purchase_order(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)
    #ExpressionFormSet = formset_factory(ExpressionForm, extra=0)
    #ExpressionFormSet.title = _(u'expressions')
    ItemsFormSet = formset_factory(PRIMakePOIForm, extra=0)

    
    if request.method == 'POST':
        formset = ItemsFormSet(request.POST)
    
    else:
    
        initial = []
        for item in purchase_request.purchaserequestitem_set.all():
            initial.append({
                'item_template':item.item_template,
                #'template_id':item.item_template.id,
                #'name':item.item_template,
                #'suppliers':item.item_template.suppliers.all()
                
            })
            print item.item_template.suppliers.all()    
        #form = PRIMakePOIForm(initial={'name':'s'})
        formset = ItemsFormSet(initial=initial)
    #item_template = purchase_request.purchaserequestitem_set.all()[0])
    #messages.success(request, "This purchase request has already been closed.")
    return render_to_response('generic_form.html', {
        'formset':formset,
    }, context_instance=RequestContext(request))  



#                initial=[]
#            for num, field in enumerate(self.settings['model']._meta.fields):
#                if field.name != 'id':
#                    initial.append({
#                        'model_field':field.name,
#                        'expression':'"%%s" %% csv_column[%s]' % str(num-1),
#                        'enabled':field.name != 'id' and True
#                        })


def purchase_order_view(request, object_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)
    form = PurchaseOrderForm_view(instance=purchase_order)
    
    return render_to_response('generic_detail.html', {
        'title':_(u'details for purchase order: %s') % purchase_order,
        'object':purchase_order,
        'form':form,
        'subtemplates_dict':[{
            'name':'generic_list_subtemplate.html',
            'title':_(u'purchase order items'),
            'object_list':purchase_order.purchaseorderitem_set.all(),
            'extra_columns':[
                {'name':_(u'qty'), 'attribute':'qty'},
                {'name':_(u'amount received'), 'attribute':'received_qty'},
                {'name':_(u'agreed price'), 'attribute':lambda x: '$%s' % x.agreed_price if x.agreed_price else '-'},
                {'name':_(u'status'), 'attribute':'status'},
                {'name':_(u'active'), 'attribute':lambda x: _(u'Open') if x.active == True else _(u'Closed')}
            ],
            #'extra_columns':[{'name':'type', 'attribute':lambda x:x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]}],
        }]
    },
    context_instance=RequestContext(request))


def purchase_order_close(request, object_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)    
    items = purchase_order.purchaseorderitem_set.all()

    data = {
        'object':purchase_order,
        'title':_(u"Are you sure you wish to close the purchase order: %s?") % purchase_order,
    }
    if items.filter(active=True):
        data['message'] = _(u'There are still open items.')
        
        
    if purchase_order.active == False:
        msg = _(u'This purchase order has already been closed.')
        messages.error(request, msg, fail_silently=True)            
        return redirect(purchase_order.get_absolute_url())
        
    
    if request.method == 'POST':
        purchase_order.active = False
        items.update(active=False)
        purchase_order.save()
        msg = _(u'The purchase order has been closed successfully.')
        messages.success(request, msg, fail_silently=True)            
        return redirect(purchase_order.get_absolute_url())

    return render_to_response('generic_confirm.html', data,
    context_instance=RequestContext(request))  


def purchase_order_open(request, object_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)    

    data = {
        'object':purchase_order,
        'title':_(u"Are you sure you wish to open the purchase order: %s?") % purchase_order,
    }
        
    if purchase_order.active == True:
        msg = _(u'This purchase order is already open.')
        messages.error(request, msg, fail_silently=True)      
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_order.get_absolute_url())
        
    if request.method == 'POST':
        purchase_order.active = True
        purchase_order.save()
        msg = _(u'The purchase order has been opened successfully.')
        messages.success(request, msg, fail_silently=True)            
        return redirect(purchase_order.get_absolute_url())

    return render_to_response('generic_confirm.html', data,
    context_instance=RequestContext(request))  


def purchase_order_item_close(request, object_id):
    purchase_order_item = get_object_or_404(PurchaseOrderItem, pk=object_id)    
    data = {
        'object':purchase_order_item,
        'title':_(u"Are you sure you wish close the purchase item order: %s?") % purchase_order_item,
    }
    
    if purchase_order_item.active == False:
        msg = _(u'This purchase order item has already been closed.')
        messages.error(request, msg, fail_silently=True)            
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_order.get_absolute_url())
        
    
    if request.method == 'POST':
        purchase_order_item.active = False
        purchase_order_item.save()
        msg = _(u'The purchase order item has been closed successfully.')
        messages.success(request, msg, fail_silently=True)            
        return redirect(purchase_order_item.get_absolute_url())

    return render_to_response('generic_confirm.html', data,
    context_instance=RequestContext(request))  


def purchase_order_item_create(request, object_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)
    
    if request.method == 'POST':
        form = PurchaseOrderItemForm(request.POST)#, initial={'purchase_order':purchase_order})
        if form.is_valid():
            form.save()
            msg = _(u'The purchase order item was created successfully.')
            messages.success(request, msg, fail_silently=True)            
            return redirect(purchase_order.get_absolute_url())
    else:
        form = PurchaseOrderItemForm(initial={'purchase_order':purchase_order})

    return render_to_response('generic_form.html', {
        'form':form,
        'title':_(u'add new purchase order item') ,
    },
    context_instance=RequestContext(request))
