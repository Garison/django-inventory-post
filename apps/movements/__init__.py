from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu

from models import PurchaseRequestStatus, PurchaseRequest, PurchaseRequestItem

purchase_request_state_list = {'text':_('purchase request states'), 'view':'purchase_request_state_list', 'famfam':'pencil_go'}
purchase_request_state_create = {'text':_('create new state'), 'view':'purchase_request_state_create', 'famfam':'pencil_add'}
purchase_request_state_update = {'text':_('edit state'), 'view':'purchase_request_state_update', 'args':'object.id', 'famfam':'pencil'}
purchase_request_state_delete = {'text':_('delete state'), 'view':'purchase_request_state_delete', 'args':'object.id', 'famfam':'pencil_delete'}

purchase_request_list = {'text':_('purchase requests'), 'view':'purchase_request_list', 'famfam':'basket_go'}
purchase_request_create = {'text':_('create new request'), 'view':'purchase_request_create', 'famfam':'basket_add'}
purchase_request_update = {'text':_('edit request'), 'view':'purchase_request_update', 'args':'object.id', 'famfam':'basket_edit'}
purchase_request_delete = {'text':_('delete request'), 'view':'purchase_request_delete', 'args':'object.id', 'famfam':'basket_delete'}

purchase_request_item_create = {'text':_('add new item'), 'view':'purchase_request_item_create', 'args':'object.id', 'famfam':'basket_put'}
purchase_request_item_update = {'text':_('edit item'), 'view':'purchase_request_item_update', 'args':'object.id', 'famfam':'basket_go'}
purchase_request_item_delete = {'text':_('delete item'), 'view':'purchase_request_item_delete', 'args':'object.id', 'famfam':'basket_remove'}


register_links(PurchaseRequestStatus, [purchase_request_state_update, purchase_request_state_delete])

register_links(PurchaseRequest, [purchase_request_update, purchase_request_delete, purchase_request_item_create])
register_links(['purchase_request_list', 'purchase_request_create', 'purchase_request_update', 'purchase_request_delete', 'purchase_request_view'], [purchase_request_create], menu_name='sidebar')

register_links(PurchaseRequestItem, [purchase_request_item_update, purchase_request_item_delete])

register_links(['purchase_request_item_create'], [purchase_request_create], menu_name='sidebar')


register_menu([
    {'text':_('purchases'), 'view':'purchase_request_list', 'links':[
        purchase_request_list, purchase_request_create
    ],'famfam':'basket','position':4}])

