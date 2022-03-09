from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model to represent users"""
    watching = models.ManyToManyField("Listing", related_name="watchers")


class Category(models.Model):
    """This model represents different categories of items"""
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name


class Listing(models.Model):
    """This model represents the auction listings"""
    title = models.CharField(max_length=64)
    description = models.TextField()
    current_price = models.DecimalField(max_digits=6, decimal_places=2)  # reference: https://stackoverflow.com/questions/1139393/what-is-the-best-django-model-field-to-use-to-represent-a-us-dollar-amount
    is_active = models.BooleanField(default=True)
    picture = models.URLField(null=True, blank=True)
    picture_text = models.CharField(blank=True, default="", max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    closed = models.BooleanField(default=False)


class Bid(models.Model):
    """This model creates the fields required for bidding"""
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return str(self.amount)


class Comment(models.Model):
    """This model creates fields required for commenting on listings"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text_comment = models.TextField(max_length=128)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
