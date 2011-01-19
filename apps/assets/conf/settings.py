from django.conf import settings
 

MAX_ASSET_PHOTOS = getattr(settings, 'ASSETS_MAX_ASSET_PHOTOS', 5)
MAX_PERSON_PHOTOS = getattr(settings, 'ASSETS_MAX_PERSON_PHOTOS', 5)
