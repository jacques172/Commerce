from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listing, comment, Bid


def index(request):
    listings = Listing.objects.filter(isActive = True)
    category = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": category
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "GET":

        category = Category.objects.all()
        return render(request, "auctions/create.html",{
        "category": category
    })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        ImageUrl = request.POST["ImageUrl"]
        category = request.POST["category"]
        price = request.POST["price"]
        currentUser = request.user
        categoryData = Category.objects.get(categoryName = category)
        priceData = Bid(user = currentUser, bid = price)
        priceData.save()
        new_listing = Listing(
            title = title,
            description = description,
            ImageUrl = ImageUrl,
            category = categoryData,
            owner = currentUser,
            price = priceData

        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))

def categories(request):
    category = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "category": category
    })
def category(request):
    if request.method == "GET":
        categoryName = request.GET["category"]
        category = Category.objects.get(categoryName = categoryName)
        listings = Listing.objects.filter(isActive = True, category = category)
        category = Category.objects.all()
        return render(request, "auctions/index.html",{

        "listings":listings,
        "category": category
        }
        )

def Listing_page(request, id):
    listingData = Listing.objects.get(pk = id)
    comments = comment.objects.filter(product = listingData)
    if request.user in listingData.watchlist.all():
        isListingInWatchlist = True
    else: 
        isListingInWatchlist = False
    isOwner = request.user.username == listingData.owner.username 
    return render(request, "auctions/Listing_page.html",{
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": comments,
        "isOwner":isOwner
    })   

def remove_watchlist(request, id):
   
        listingData = Listing.objects.get(id = id)
        currentUser = request.user
        listingData.watchlist.remove(currentUser)
        return HttpResponseRedirect(reverse("Listing_page", kwargs = {"id": id}))
    
def add_watchlist(request, id):
    
        listingData = Listing.objects.get(id = id)
        currentUser = request.user
        listingData.watchlist.add(currentUser)
        return HttpResponseRedirect(reverse("Listing_page", kwargs = {"id": id }))

def watchlist(request):
    currentUser = request.user
    listings = currentUser.watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })

def add_comment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk = id)
    message = request.POST["comment"]

    new_comment = comment(user = currentUser, product = listingData, comment = message)
    new_comment.save()
    return HttpResponseRedirect(reverse("Listing_page", args = (id, )))

def addBid(request, id):
    newBid = request.POST["newBid"]
    listingData = Listing.objects.get(pk = id)
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user = request.user, bid = newBid)
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/Listing_page.html", {
                "listing": listingData,
                "message": "Bid updated successfully",
                "update": True

        })
    else:
        return render(request, "auctions/Listing_page.html", {
                "listing": listingData,
                "message": "Bid update failed",
                "update": False})

def close_auction(request, id):
    listingData = Listing.objects.get(pk = id)
    isOwner = request.user.username == listingData.owner.username 
    listingData.isActive = False
    listingData.save()
    isListingInWatchlist = request.user in listingData.watchlist.all()
    comments = comment.objects.filter(product = listingData)
    return render(request, "auctions/Listing_page.html", {
            "listing": listingData,
            "message": "Congratulations!, your auction is closed",
            "update": True,
            "isOwner":isOwner,
            "allComment":comments,
            "isListingInWatchlist":isListingInWatchlist
    })
    

