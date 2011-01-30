from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object

from generic_views.views import generic_assign_remove, \
                                generic_delete, \
                                generic_detail, generic_list

from models import PurchaseRequestStatus, PurchaseRequest, \
                   PurchaseRequestItem, PurchaseOrderStatus, \
                   PurchaseOrderItemStatus, PurchaseOrder, \
                   PurchaseOrderItem

from movements import purchase_request_state_filter, \
                      purchase_order_state_filter


urlpatterns = patterns('movements.views',
    url(r'^purchase/request/state/list/$', generic_list, dict({'queryset':PurchaseRequestStatus.objects.all()}, extra_context=dict(title =_(u'purchase request states'), create_view='purchase_request_state_create')), 'purchase_request_state_list'),
    url(r'^purchase/request/state/create/$', create_object,{'model':PurchaseRequestStatus, 'template_name':'generic_form.html', 'extra_context':{'title':_(u'create new purchase request state')}}, 'purchase_request_state_create'),
    url(r'^purchase/request/state/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseRequestStatus, 'template_name':'generic_form.html'}, 'purchase_request_state_update'),
    url(r'^purchase/request/state/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseRequestStatus}, post_delete_redirect="purchase_request_state_list", extra_context=dict(object_name=_(u'purchase request state'))), 'purchase_request_state_delete'),

    url(r'^purchase/request/list/$', generic_list, dict({'queryset':PurchaseRequest.objects.all(), 'list_filters':[purchase_request_state_filter]}, extra_context=dict(title =_(u'purchase requests'), extra_columns = [{'name':_(u'Active'), 'attribute':lambda x: _(u'Open') if x.active == True else _(u'Closed')}])), 'purchase_request_list'),
    url(r'^purchase/request/(?P<object_id>\d+)/$', 'purchase_request_view', (), 'purchase_request_view'),
    url(r'^purchase/request/create/$', create_object,{'model':PurchaseRequest, 'template_name':'generic_form.html', 'extra_context':{'title':_(u'create new purchase request')}}, 'purchase_request_create'),
    url(r'^purchase/request/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseRequest, 'template_name':'generic_form.html'}, 'purchase_request_update'),
    url(r'^purchase/request/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseRequest}, post_delete_redirect="purchase_request_list", extra_context=dict(object_name=_(u'purchase request'))), 'purchase_request_delete'),
    url(r'^purchase/request/(?P<object_id>\d+)/close/$', 'purchase_request_close', (), 'purchase_request_close'),
    url(r'^purchase/request/(?P<object_id>\d+)/open/$', 'purchase_request_open', (), 'purchase_request_open'),
    url(r'^purchase/request/(?P<object_id>\d+)/make_purchase_order/$', 'purchase_request_make_purchase_order', (), 'purchase_request_make_purchase_order'),

    url(r'^purchase/request/(?P<object_id>\d+)/add_item/$', 'purchase_request_item_create', (), 'purchase_request_item_create'),
    url(r'^purchase/request/item/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseRequestItem, 'template_name':'generic_form.html'}, 'purchase_request_item_update'),
    url(r'^purchase/request/item/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseRequestItem}, post_delete_redirect="purchase_request_list", extra_context=dict(object_name=_(u'purchase request item'))), 'purchase_request_item_delete'),

    url(r'^purchase/order/state/list/$', generic_list, dict({'queryset':PurchaseOrderStatus.objects.all()}, extra_context=dict(title =_(u'purchase order states'), create_view='purchase_order_state_create')), 'purchase_order_state_list'),
    url(r'^purchase/order/state/create/$', create_object,{'model':PurchaseOrderStatus, 'template_name':'generic_form.html', 'extra_context':{'title':_(u'create new purchase order state')}}, 'purchase_order_state_create'),
    url(r'^purchase/order/state/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseOrderStatus, 'template_name':'generic_form.html'}, 'purchase_order_state_update'),
    url(r'^purchase/order/state/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseOrderStatus}, post_delete_redirect="purchase_order_state_list", extra_context=dict(object_name=_(u'purchase order status'))), 'purchase_order_state_delete'),

    url(r'^purchase/order/list/$', generic_list, dict({'queryset':PurchaseOrder.objects.all(), 'list_filters':[purchase_order_state_filter]}, extra_context=dict(title =_(u'purchase orders'), extra_columns = [{'name':_(u'Active'), 'attribute':lambda x: _(u'Open') if x.active == True else _(u'Closed')}])), 'purchase_order_list'),
    url(r'^purchase/order/(?P<object_id>\d+)/$', 'purchase_order_view', (), 'purchase_order_view'),
    url(r'^purchase/order/create/$', create_object,{'model':PurchaseOrder, 'template_name':'generic_form.html', 'extra_context':{'title':_(u'create new purchase order')}}, 'purchase_order_create'),
    url(r'^purchase/order/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseOrder, 'template_name':'generic_form.html'}, 'purchase_order_update'),
    url(r'^purchase/order/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseOrder}, post_delete_redirect="purchase_order_list", extra_context=dict(object_name=_(u'purchase order'))), 'purchase_order_delete'),
    url(r'^purchase/order/(?P<object_id>\d+)/close/$', 'purchase_order_close', (), 'purchase_order_close'),
    url(r'^purchase/order/(?P<object_id>\d+)/open/$', 'purchase_order_open', (), 'purchase_order_open'),

    url(r'^purchase/order/item/state/list/$', generic_list, dict({'queryset':PurchaseOrderItemStatus.objects.all()}, extra_context=dict(title =_(u'purchase order item states'), create_view='purchase_order_item_state_create')), 'purchase_order_item_state_list'),
    url(r'^purchase/order/item/state/create/$', create_object,{'model':PurchaseOrderItemStatus, 'template_name':'generic_form.html', 'extra_context':{'title':_(u'create new purchase order item state')}}, 'purchase_order_item_state_create'),
    url(r'^purchase/order/item/state/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseOrderItemStatus, 'template_name':'generic_form.html'}, 'purchase_order_item_state_update'),
    url(r'^purchase/order/item/state/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseOrderItemStatus}, post_delete_redirect="purchase_order_item_state_list", extra_context=dict(object_name=_(u'purchase order item status'))), 'purchase_order_item_state_delete'),

    url(r'^purchase/order/(?P<object_id>\d+)/add_item/$', 'purchase_order_item_create', (), 'purchase_order_item_create'),
    url(r'^purchase/order/item/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseOrderItem, 'template_name':'generic_form.html'}, 'purchase_order_item_update'),
    url(r'^purchase/order/item/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseOrderItem}, post_delete_redirect="purchase_order_list", extra_context=dict(object_name=_(u'purchase order item'))), 'purchase_order_item_delete'),
    url(r'^purchase/order/item/(?P<object_id>\d+)/close/$', 'purchase_order_item_close', (), 'purchase_order_item_close'),

)
    

