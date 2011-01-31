import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse

from photos.models import GenericPhoto

from dynamic_search.api import register


class Location(models.Model):
    name = models.CharField(max_length=32, verbose_name=_("name"))
    address_line1 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'address'))
    address_line2 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'address'))
    address_line3 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'address'))
    address_line4 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'address'))
    phone_number1 = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'phone number'))
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'phone number'))

    class Meta:
        ordering = ['name']
        verbose_name = _(u"location")
        verbose_name_plural = _(u"locations")
        
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('location_view', [str(self.id)])
    
                
class ItemTemplate(models.Model):
    description = models.CharField(verbose_name=_(u"description"), max_length=64)
    brand = models.CharField(verbose_name=_(u"brand"), max_length=32, null=True, blank=True)
    model = models.CharField(verbose_name=_(u"model"), max_length=32, null=True, blank=True)
    part_number = models.CharField(verbose_name=_(u"part number"), max_length=32, null=True, blank=True)
    notes = models.TextField(verbose_name=_(u"notes"), null=True, blank=True)	
    supplies = models.ManyToManyField("self", null=True, blank=True, verbose_name=_(u"supplies"))
    suppliers = models.ManyToManyField("Supplier", null=True, blank=True)
    
    class Meta:
        ordering = ['description']	
        verbose_name = _(u"item template")
        verbose_name_plural = _(u"item templates")        
    
    @models.permalink
    def get_absolute_url(self):
        return ('template_view', [str(self.id)])
    
    def __unicode__(self):
        return self.description

   
class Log(models.Model):
    timedate = models.DateTimeField(auto_now_add=True, verbose_name=_(u"timedate"))
    action = models.CharField(max_length=32)
    description = models.TextField(verbose_name=_(u"description"), null=True, blank=True)
    #user = models.ForeignKey(User, unique=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    def __unicode__(self):
#		return "%Y-%m-%d %H:%M:%S" % (self.timedate) #& user  && item
        return "%s, %s - %s" % (self.timedate, self.action, self.content_object)

    @models.permalink
    def get_absolute_url(self):
        return ('log_view', [str(self.id)])


class Inventory(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'name'))
    location = models.ForeignKey(Location, verbose_name=_(u'location'))

    class Meta:
        verbose_name = _(u'inventory')
        verbose_name_plural = _(u'inventories')

    @models.permalink
    def get_absolute_url(self):
        return ('inventory_view', [str(self.id)])

    def __unicode__(self):
        return self.name


class InventoryCheckPoint(models.Model):
    inventory = models.ForeignKey(Inventory)
    datetime = models.DateTimeField(default=datetime.datetime.now())	
    supplies = models.ManyToManyField(ItemTemplate, null=True, blank=True, through='InventoryCPQty')


class InventoryCPQty(models.Model):
    supply = models.ForeignKey(ItemTemplate)
    check_point = models.ForeignKey(InventoryCheckPoint)
    quantity = models.IntegerField()

    
class InventoryTransaction(models.Model):
    inventory = models.ForeignKey(Inventory)
    supply = models.ForeignKey(ItemTemplate)
    quantity = models.IntegerField()
    date = models.DateField(default=datetime.date.today(), verbose_name=_(u"date"))
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = _(u'inventory transaction')
        verbose_name_plural = _(u'inventory transactions')
        ordering = ['-date']

    @models.permalink
    def get_absolute_url(self):
        return ('inventory_transaction_view', [str(self.id)])
    
    def __unicode__(self):
        return "%s: '%s' qty=%s @ %s" % (self.inventory, self.supply, self.quantity, self.date)


class Supplier(models.Model):
    #TODO: Contact, extension
    name = models.CharField(max_length=32, verbose_name=_("name"))
    address_line1 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'address'))
    address_line2 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'address'))
    address_line3 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'address'))
    address_line4 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'address'))
    phone_number1 = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'phone number'))
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'phone number'))
    notes = models.TextField(null=True, blank=True, verbose_name=(u'notes'))
    
    class Meta:
        ordering = ['name']
        verbose_name = _(u"supplier")
        verbose_name_plural = _(u"suppliers")
        
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])

register(ItemTemplate, _(u'templates'), ['description', 'brand', 'model', 'part_number', 'notes'])
register(Location, _(u'locations'), ['name', 'address_line1', 'address_line2', 'address_line3', 'address_line4', 'phone_number1', 'phone_number2'])
register(Inventory, _(u'inventory'), ['name', 'location__name'])
register(Supplier, _(u'supplier'), ['name', 'address_line1', 'address_line2', 'address_line3', 'address_line4', 'phone_number1', 'phone_number2', 'notes'])
