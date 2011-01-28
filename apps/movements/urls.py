from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object

from generic_views.views import generic_assign_remove, \
                                generic_delete, \
                                generic_detail, generic_list

from models import PurchaseRequestStatus, PurchaseRequest, PurchaseRequestItem

urlpatterns = patterns('movements.views',
    url(r'^purchase/request/state/list/$', generic_list, dict({'queryset':PurchaseRequestStatus.objects.all()}, extra_context=dict(title =_(u'purchase request states'), create_view='purchase_request_state_create')), 'purchase_request_state_list'),
    url(r'^purchase/request/state/create/$', create_object,{'model':PurchaseRequestStatus, 'template_name':'generic_form.html', 'extra_context':{'title':_(u'create new purchase request state')}}, 'purchase_request_state_create'),
    url(r'^purchase/request/state/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseRequestStatus, 'template_name':'generic_form.html'}, 'purchase_request_state_update'),
    url(r'^purchase/request/state/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseRequestStatus}, post_delete_redirect="purchase_request_state_list", extra_context=dict(title=_(u'purchase request state'))), 'purchase_request_state_delete'),

    url(r'^purchase/request/list/$', generic_list, dict({'queryset':PurchaseRequest.objects.all()}, extra_context=dict(title =_(u'purchase request'), create_view='purchase_request_create')), 'purchase_request_list'),
    #url(r'^purchase/request/(?P<object_id>\d+)/$', generic_detail, dict(form_class=InventoryForm, queryset=Inventory.objects.all()), 'purchase_request_view'),
    url(r'^purchase/request/(?P<object_id>\d+)/$', 'purchase_request_view', (), 'purchase_request_view'),
    url(r'^purchase/request/create/$', create_object,{'model':PurchaseRequest, 'template_name':'generic_form.html', 'extra_context':{'title':_(u'create new purchase request')}}, 'purchase_request_create'),
    url(r'^purchase/request/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseRequest, 'template_name':'generic_form.html'}, 'purchase_request_update'),
    url(r'^purchase/request/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseRequest}, post_delete_redirect="purchase_request_list", extra_context=dict(title=_(u'purchase request'))), 'purchase_request_delete'),

    url(r'^purchase/request/(?P<object_id>\d+)/add_item/$', 'purchase_request_item_create', (), 'purchase_request_item_create'),
    url(r'^purchase/request/item/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseRequestItem, 'template_name':'generic_form.html'}, 'purchase_request_item_update'),
    url(r'^purchase/request/item/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseRequestItem}, post_delete_redirect="purchase_request_list", extra_context=dict(title=_(u'purchase request'))), 'purchase_request_item_delete'),

)
    

