from django.utils.translation import ugettext_lazy as _

purchase_request_state_list = {'text':_('purchase request states'), 'view':'purchase_request_state_list'}#, 'famfam':'package_go'}
purchase_request_state_create = {'text':_('create new state'), 'view':'purchase_request_state_create'}#, 'famfam':'package_go'}
purchase_request_state_update = {'text':_('edit state'), 'view':'purchase_request_state_update'}#, 'famfam':'package_go'}
purchase_request_state_delete = {'text':_('delete state'), 'view':'purchase_request_state_delete'}#, 'famfam':'package_go'}

purchase_request_state_record_links = [
    purchase_request_state_update, purchase_request_state_delete
    ]
