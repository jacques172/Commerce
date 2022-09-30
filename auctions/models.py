from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, blank= True, null = True, related_name = "user_bid")  
    bid = models.FloatField(default = 0)
    def __str__(self):
        return f"{self.bid}"

class Listing(models.Model):
    title = models.CharField(max_length= 32)
    owner = models.ForeignKey(User, on_delete= models.CASCADE, blank= True, null = True, related_name = "user")
    ImageUrl = models.CharField(max_length= 100000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank = True, null = True, related_name = "price")
    category = models.ForeignKey(Category, on_delete= models.CASCADE, blank= True, null = True, related_name = "category")
    description = models.CharField(max_length= 1000)
    isActive =  models.BooleanField(default = True)
    watchlist = models.ManyToManyField(User, blank = True, null = True, related_name = "watchlist")
    

    def __str__(self):
        return self.title

class comment(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, blank= True, null = True, related_name = "user_comment")
    product = models.ForeignKey(Listing, on_delete= models.CASCADE, blank= True, null = True, related_name = "product_comment")
    comment = models.CharField(max_length = 1000)
    def __str__(self):
        return f"{self.user}({self.product})"
