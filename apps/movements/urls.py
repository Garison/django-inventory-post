from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import create_object, update_object

from generic_views.views import generic_assign_remove, \
                                generic_delete, \
                                generic_detail, generic_list

from models import PurchaseRequestStatus 
from movements import purchase_request_state_record_links

#from inventory import location_filter

#from assets import person_record_links, asset_record_links, state_record_links, group_record_links
#from models import Item, ItemGroup, Person, State
#from forms import ItemForm, ItemForm_view, ItemGroupForm, PersonForm, PersonForm_view

urlpatterns = patterns('movements.views',
    url(r'^purchase/request/state/list/$', generic_list, dict({'queryset':PurchaseRequestStatus.objects.all()}, extra_context=dict(title =_(u'purchase request states'), create_view='purchase_request_state_create', record_links=purchase_request_state_record_links)), 'purchase_request_state_list'),
    url(r'^purchase/request/state/create/$', create_object,{'model':PurchaseRequestStatus, 'template_name':'generic_form.html', 'extra_context':{'title':_(u'create new purchase request state')}}, 'purchase_request_state_create'),
    url(r'^purchase/request/state/(?P<object_id>\d+)/update/$', update_object, {'model':PurchaseRequestStatus, 'template_name':'generic_form.html'}, 'purchase_request_state_update'),
    url(r'^purchase/request/state/(?P<object_id>\d+)/delete/$', generic_delete, dict({'model':PurchaseRequestStatus}, post_delete_redirect="purchase_request_state_list", extra_context=dict(title=_(u'purchase request state'))), 'purchase_request_state_delete'),
)
    

