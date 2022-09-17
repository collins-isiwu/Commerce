from django.contrib import admin
from .models import Listing, Bids, Comments

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Comments)