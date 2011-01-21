from django.utils.translation import ugettext_lazy as _

from models import State

state_list = {'text':_('assets states'), 'view':'state_list', 'famfam':'error_go'}
state_edit = {'text':_(u'edit asset state'), 'view':'state_update', 'famfam':'error'}
state_delete = {'text':_(u'delete asset state'), 'view':'state_delete', 'famfam':'error_delete'}

state_record_links = [
    state_edit, state_delete
]

person_list = {'text':_('view all people'), 'view':'person_list', 'famfam':'user_go'}
person_create = {'text':_('create new person'), 'view':'person_create', 'famfam':'user_add'}
person_update = {'text':_(u'edit'), 'view':'person_update', 'famfam':'user_edit'}
person_delete = {'text':_(u'delete'), 'view':'person_delete', 'famfam':'user_delete'}
person_photos = {'text':_(u'edit photos'), 'view':'person_photos', 'famfam':'picture_edit'}
person_assign_item = {'text':_(u'assign assets'), 'view':'person_assign_item', 'famfam':'computer_go'}

person_record_links = [
    person_update, person_delete, person_photos, person_assign_item
]

asset_list = {'text':_('view all assets'), 'view':'item_list', 'famfam':'computer'}
asset_create = {'text':_('create new asset'), 'view':'item_create', 'famfam':'computer_add'}
asset_orphan_list = {'text':_('orphan assets'), 'view':'item_orphans_list'}
asset_edit = {'text':_(u'edit'), 'view':'item_update', 'famfam':'computer_edit'}
asset_delete = {'text':_(u'delete'), 'view':'item_delete', 'famfam':'computer_delete'}
asset_photos = {'text':_(u'photos'), 'view':'item_photos', 'famfam':'picture_edit'}
asset_assign_person = {'text':_(u'assign people'), 'view':'item_assign_person', 'famfam':'user_go'}
asset_template = {'text':_(u'template'), 'view':'template_view', 'args':'object.item_template.id', 'famfam':'page_go'}


asset_record_links = [
    asset_edit, asset_delete, asset_photos, asset_assign_person, asset_template
]

group_list = {'text':_(u'view all groups'), 'view':'group_list'}
group_create = {'text':_(u'create group'), 'view':'group_create'}
group_update = {'text':_(u'edit'), 'view':'group_update'}
group_delete = {'text' : _(u'delete'), 'view':'group_delete'}

group_record_links = [
    group_update, group_delete
]

state_filter = {'name':'state', 'queryset':State.objects.all(), 'destination':'itemstate'}
