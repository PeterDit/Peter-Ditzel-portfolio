from django.contrib import admin

# Register your models here.

from .models import User, Bid, Listing, watchlistmodel, Category

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(watchlistmodel)
admin.site.register(Category)






