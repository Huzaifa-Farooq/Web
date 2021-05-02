from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    CATEGORY_CHOICES = [
        ("No Category Listed", "No Category Listed"),
        ("Fashion", "Fashion"),
        ("Home", "Home"),
        ("Electronics", "Electronics"),
        ("'Health & Beauty", "'Health & Beauty"),
        ("Sports & Outdoor", "Sports & Outdoor"),
        ("Education", "Education"),
    ]

    title = models.CharField(max_length=24)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, default="None", blank=True)
    created_by = models.ForeignKey("auctions.User", on_delete=models.CASCADE, related_name="listings")
    starting_bid = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    datetime = datetime.datetime.now()


    def __str__(self):
        return f"ID: {self.id}: Title: {self.title}"

class AuctionBids(models.Model):
    listingid = models.ForeignKey("auctions.AuctionListing", on_delete=models.CASCADE, related_name="listings_bids")
    user = models.ForeignKey("auctions.User", on_delete=models.CASCADE, related_name="user_bids")
    current_bid = models.PositiveIntegerField()

    def __str__(self):
        return f" {self.listingid} User: {self.user}, Bid: {self.current_bid}"

class Watchlist(models.Model):
    listing_id = models.ForeignKey("auctions.AuctionListing", on_delete=models.CASCADE, related_name="listings_watchlist")
    user = models.ForeignKey("auctions.User", on_delete=models.CASCADE, related_name="user_watchlist")

    def __str__(self):
        return f"User: {self.user} Listing {self.listing_id}"

class Comments(models.Model):
    comment = models.CharField(max_length=200)
    listing_id = models.ForeignKey("auctions.AuctionListing", on_delete=models.CASCADE, related_name="listings_comments")
    user = models.ForeignKey("auctions.User", on_delete=models.CASCADE, related_name="user_comments")
    datetime = datetime.datetime.now()

    def __str__(self):
        return f"{self.user.username}: {self.comment}, Listing ID: {self.listing_id}"

