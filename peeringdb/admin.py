from __future__ import unicode_literals

from django.contrib import admin
from .models import Network, NetworkIXLAN, Synchronization

admin.site.register(Network)
admin.site.register(NetworkIXLAN)
admin.site.register(Synchronization)