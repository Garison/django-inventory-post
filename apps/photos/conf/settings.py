from django.conf import settings

MAX_PHOTO_SIZE = getattr(settings, 'PHOTOS_MAX_PHOTO_SIZE', 1000000)

