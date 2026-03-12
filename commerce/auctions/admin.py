from django.contrib import admin
from .models import auction_listing, bid, Category, comments

# Register your models here.
admin.site.register(auction_listing)
admin.site.register(bid)
admin.site.register(Category)
admin.site.register(comments)