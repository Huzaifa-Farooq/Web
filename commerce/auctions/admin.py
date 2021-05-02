from django.contrib import admin
from .models import AuctionListing, AuctionBids, Comments, Watchlist
# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(AuctionBids)
admin.site.register(Comments)
admin.site.register(Watchlist)