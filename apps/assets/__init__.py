from django.utils.translation import ugettext_lazy as _

state_list = {'text':_('states'), 'view':'state_list', 'famfam':'error_go'}
state_edit = {'text':_(u'edit'), 'view':'state_update'}
state_delete = {'text':_(u'delete'), 'view':'state_delete'}

state_record_links = [
    state_edit, state_delete
]

person_list = {'text':_('view all people'), 'view':'person_list'}
person_create = {'text':_('create new person'), 'view':'person_create'}
person_update = {'text':_(u'edit'), 'view':'person_update'}
person_delete = {'text':_(u'delete'), 'view':'person_delete'}
person_photos = {'text':_(u'edit photos'), 'view':'person_photos'}
person_assign_item = {'text':_(u'assign/remove asset'), 'view':'person_assign_item'}

person_record_links = [
    person_update, person_delete, person_photos, person_assign_item
]

asset_list = {'text':_('view all assets'), 'view':'item_list'}
asset_create = {'text':_('create new asset'), 'view':'item_create'}
asset_orphan_list = {'text':_('orphans assets'), 'view':'item_orphans_list'}
asset_edit = {'text':_(u'edit'), 'view':'item_update'}
asset_delete = {'text':_(u'delete'), 'view':'item_delete'}
asset_photos = {'text':_(u'photos'), 'view':'item_photos'}
asset_assign_person = {'text':_(u'assign/remove people'), 'view':'item_assign_person'}
asset_template = {'text':_(u'template'), 'view':'template_view', 'args':'object.item_template.id'}


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
