from django.utils.translation import ugettext_lazy as _

from common.api import register_links

from models import PurchaseRequestStatus

purchase_request_state_list = {'text':_('purchase request states'), 'view':'purchase_request_state_list', 'famfam':'pencil_go'}
purchase_request_state_create = {'text':_('create new state'), 'view':'purchase_request_state_create', 'famfam':'pencil_add'}
purchase_request_state_update = {'text':_('edit state'), 'view':'purchase_request_state_update', 'args':'object.id', 'famfam':'pencil'}
purchase_request_state_delete = {'text':_('delete state'), 'view':'purchase_request_state_delete', 'args':'object.id', 'famfam':'pencil_delete'}

register_links(PurchaseRequestStatus, [purchase_request_state_update, purchase_request_state_delete])
