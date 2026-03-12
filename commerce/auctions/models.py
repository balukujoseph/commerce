from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=61)
    def __str__(self):
        return self.name
    
class auction_listing(models.Model):
    image_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=63)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watched_list")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", blank="True", null="True")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    
    def __str__(self):
        return f"{self.name} {self.price} {self.date_created}"
    
class bid(models.Model):
    auction_listing = models.ForeignKey(auction_listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()
    
    def __str__(self):
        return f"{self.user.username} bid ${self.amount} on {self.auction_listing}"
    
class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    auction_listing = models.ForeignKey(auction_listing, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.auction_listing}: {self.message}"