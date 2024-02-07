from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Category(models.Model):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=128)
    starting_bid = models.IntegerField(validators=[MinValueValidator(10)])
    url = models.CharField(max_length=128)
    category = models.ManyToManyField(Category, blank=True, related_name="listings")


class Bid(models.Model):
    pass

class Comment(models.Model):
    pass