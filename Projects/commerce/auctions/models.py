from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, URLValidator

class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_listings")
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=128)
    starting_bid = models.IntegerField(validators=[MinValueValidator(10)])
    greater_bid = models.IntegerField(default=0)
    url = models.CharField(max_length=128, validators=[URLValidator()], blank=True)
    category = models.ManyToManyField(Category, related_name="listings")
    status = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="won_listings")

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    value = models.IntegerField(validators=[MinValueValidator(10)])

    def __str__(self):
        return f"Bid by {self.author.username} on {self.listing.title}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=256)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment by {self.author.username} on {self.listing.title}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"user {self.user.username} is watching {self.listing.title}"