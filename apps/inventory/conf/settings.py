from django.conf import settings


MAX_TEMPLATE_PHOTOS = getattr(settings, 'INVENTORY_MAX_TEMPLATE_PHOTOS', 5)
