from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Category(models.Model):
    cat_name = models.CharField(max_length=64)
    def __str__(self):
        return self.cat_name
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="bidder")
    def __float__(self):
        return float(self.bid)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000, blank=True, default="no url")
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price", default=0)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchers")
    def __str__(self):
        return self.title

class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentor")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="commented_listing")
    message = models.CharField(max_length=1000, default=" ")
    def __str__(self):
        return f"{self.commentor} wrote {self.message} on {self.listing}"


