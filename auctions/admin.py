from django.contrib import admin
from .models import User, Listing, Category, Bid

# Register your models here.
class listing_admin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "active", "owner", "category")


admin.site.register(User)
admin.site.register(Listing, listing_admin)
admin.site.register(Category)
admin.site.register(Bid)
