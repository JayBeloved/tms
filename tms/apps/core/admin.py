from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "TMS Super Admin"
admin.site.site_title = "TMS Super Admin Area"
admin.site.index_title = "Welcome to the TMS Super Admin Area"

admin.site.register(landlord)
admin.site.register(managed_properties)
admin.site.register(tenant)
admin.site.register(rentals)
