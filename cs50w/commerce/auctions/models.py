from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils import timezone


class User(AbstractUser):
    custom_field = models.CharField(max_length=100)
    # Adding a primary key to avoid warnings
    id = models.AutoField(primary_key=True) 

class Category(models.Model):
    name = models.CharField(max_length=100)
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return self.name
    
class Listing(models.Model):
    # Title of the listing
    title = models.CharField(max_length=100)
    # Description of the listing
    description = models.TextField()
    # Starting bid amount
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    # highest bid amount
    updated_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=True)
    # Image upload
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    # Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Storing the user with the created listing
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # Adding a primary key to avoid warnings
    id = models.AutoField(primary_key=True)
    # Adding a datetime
    created_at = models.DateTimeField(default=timezone.now)
    # Adding a choices
    DURATION_CHOICES = ( 
                       ("1 Day", "One Day"),
                       ("2 Days", "Two Days"),
                       ("5 Days", "Five Days"),
                       ("10 Days", "Ten Days"),)
  
    duration = models.CharField(max_length=10, choices = DURATION_CHOICES)
    # Endtime of the auction
    endtime = models.DateTimeField(auto_now_add=True)
    # Check if auction is active
    is_active = models.BooleanField(default=True)
    # Adding current datetime
    
class Bid(models.Model):
    # A decimal field for the bid amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # A foreign key field that created a relationship to the User model. If the user is deleted, all their bids will also be deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # A foreign key field that created a relationship to the AuctionListing model. If the auction listing is deleted, all associated bids will be deleted.
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    # Adding a primary key to avoid warnings
    id = models.AutoField(primary_key=True)
    
class watchlistmodel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Listing)
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return f"{self.user}'s watchlist"

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    comment = models.CharField(max_length=355)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)      