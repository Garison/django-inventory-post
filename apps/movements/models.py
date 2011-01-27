from django.db import models
from django.utils.translation import ugettext_lazy as _

from inventory.models import Supplier, ItemTemplate


class PurchaseRequestStatus(models.Model):
    name = models.CharField(verbose_name=_(u'name'), max_length=32)
    
    class Meta:
        verbose_name = _(u'purchase request status')
        verbose_name_plural = _(u'purchase request status')
        
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('purchase_request_state_list', [])
        

class PurchaseRequest(models.Model):
    issue_date = models.DateField(verbose_name=_(u'issue date'))
    required_date = models.DateField(null=True, blank=True, verbose_name=_(u'date required'))
    budget = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'budget')) 
    active = models.BooleanField(default=True, verbose_name=_(u'active'))
    status = models.ForeignKey(PurchaseRequestStatus, null=True, blank=True, verbose_name=_(u'status'))
    #originator
    #account number
    
    class Meta:
        verbose_name = _(u'purchase request')
        verbose_name_plural = _(u'purchase requests')
        
    def __unicode__(self):
        return '%s - %s' % (self.id, self.issue_date) 
        
#    @models.permalink
#    def get_absolute_url(self):
#        return ('state_list', [])



class PurchaseRequestItem(models.Model):
    #Prefered suppliers m2m
    purchase_request = models.ForeignKey(PurchaseRequest, verbose_name=_(u'purchase request'))
    item_template = models.ForeignKey(ItemTemplate, verbose_name=_(u'item template'))
    qty = models.PositiveIntegerField(verbose_name=_(u'quantity'))
    notes = models.TextField(null=True, blank=True, verbose_name=_(u'notes'))
    
    class Meta:
        verbose_name = _(u'purchase request item')
        verbose_name_plural = _(u'purchase request items')
        
    def __unicode__(self):
        return '%s - %s' % (unicode(self.item_template), self.qty)

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('purchase_request_state_list', [])

"""
ChangeOrder
"""

"""

class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, verbose_name=_(u'supplier'))
    
    
#class PurchaseOrderItem(models.Model):
#    purchase_order = models.ForeignKey(PurchaseOrder, verbose_name=_(u'purchase order'))
#    item_template = models.ForeignKey(ItemTemplate, verbose_name=_(u'item template'))
"""
