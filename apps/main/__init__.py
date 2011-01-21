from django.utils.translation import ugettext as _

import assets
import inventory

navigation = [
    {'text':_('home'), 'view':'home', 'famfam':'house'},
    {'text':_('templates'), 'view':'template_list', 'links':inventory.template_menu_links, 'famfam':'page'},
    {'text':_('assets'), 'view':'item_list', 'links':[
        assets.asset_list, assets.asset_create, assets.asset_orphan_list, assets.group_list, assets.group_create, assets.person_list, assets.person_create 
    ], 'famfam':'computer'},
    {'text':_('inventories'), 'view':'inventory_list', 'links':inventory.inventory_menu_links,'famfam':'package_go'},
    {'text':_('tools'), 'view':'location_list', 'links': [
        inventory.location_list, assets.state_list, inventory.supplier_list,
        {'text':_('import'), 'view':'import_wizard', 'famfam':'lightning_add'}
    ],'famfam':'wrench'},
    {'text':_('search'), 'view':'search', 'famfam':'zoom'},
    {'text':_('about'), 'view':'about'},
]
