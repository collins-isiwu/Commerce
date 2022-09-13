from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass

class Category(models.Model):
    categorified = models.CharField(max_length=100)

    def __str__(self):
        return self.categorified

    """ Orders categorified names alphabetically """
    class Meta:
        ordering = ['categorified']


class Listing(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=1000)
    startingBid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    active = models.BooleanField(default=True)
    image = models.URLField(max_length=1000, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings") 
    created_DT = models.DateTimeField(auto_now_add=True)
    watched_by = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f'{self.title}' and f'{self.startingBid}'

    def no_of_bid(self):
        """ Returns total number of bids submitted for a listing"""
        return self.bids.all().count()

    def highest_bid(self):
        """ solves the highest bid or if no bids, returns the starting price """
        if self.no_of_bid > 0:
            return round(self.bids.aggregate(Max('amount'))['amount_max'],2)
        else:
            return None

    def current_winner(self):
        """ resolves the user with the winning bid for the listing"""
        if self.no_of_bid > 0:
            return self.bids.get(amount=self.highest_bid()).user
        else:
            return None

    class Meta:
         """ Orders listings by the most recent created """
         ordering = ['-created_DT']

class Bids(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.amount}"

class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=7000)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)

    class order:
        """ orders comments by the most recent first"""
        ordering = ['-time']
