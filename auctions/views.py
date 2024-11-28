from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "all_listings":Listing.objects.all()
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
    
def create_listing(request):
    # return render(request, "auctions/create_listing.html")
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "categories":Category.objects.all()
        })
    if request.method == "POST":
        title = request.POST["title"]
        price = request.POST['price']
        description = request.POST['description']
        category = request.POST['category']
        if request.POST['image_url']:
            image_url = request.POST['image_url']
        elif not request.POST['image_url']:
            image_url = "no url"

        # create new bid object to put in listing
        bid = Bid(bid=float(price), user=request.user)
        bid.save()

        # create listing
        new_listing = Listing(
            title = title,
            description = description,
            image_url = image_url,
            price = bid,
            category = Category.objects.get(cat_name=category),
            owner = request.user
        )
        # save data
        new_listing.save()
        # redirect !! doesn't use httpresponse redirect (?)
        return HttpResponseRedirect(reverse("index"), {
            # "all_listings":Listing.objects.all(),
            "message":"You're listing has been successfully posted!"
        })
    
def listing(request, listing_title):
    curr_user = request.user
    curr_listing=Listing.objects.get(title=listing_title)
    inWatchlist = curr_user in curr_listing.watchlist.all()

    comments = []
    for comment in Comment.objects.all():
        if curr_listing == comment.listing:
            comments.append(comment)
        
    return render(request, "auctions/listing.html", {
        "listing_title":listing_title,
        "curr_listing": curr_listing,
        "curr_user":curr_user,
        "inWatchlist": inWatchlist,
        "comments":comments
        # if not empty, means listing is in user's watchlist
        # "watchlist":Listing.objects.get(watchlist=curr_user)
    })

def place_bid(request, listing_id):
    curr_listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        if float(request.POST['bid']) <= float(curr_listing.price):
            return render(request, "auctions/bid.html", {
                "message_error":"error",
                "listing_title":curr_listing.title
            })
        else:
            new_bid = Bid(bid=request.POST['bid'], user=request.user)
            new_bid.save()
            curr_listing.price=new_bid
            curr_listing.save()
            return render(request, "auctions/bid.html", {
                "message_succes":"succes"
            })
        
            # return render(request, "auctions/bid.html", {
            #     "message":"success"
            # })

def add_watchlist(request, listing_id):
    curr_user = request.user
    listing=Listing.objects.get(pk=listing_id)
    listing.watchlist.add(curr_user)
    listing.save
    return HttpResponseRedirect(reverse("listing", args=(listing.title, )))

def remove_watchlist(request, listing_id):
    curr_user = request.user
    listing=Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(curr_user)
    listing.save
    return HttpResponseRedirect(reverse("listing", args=(listing.title, )))

def show_watchlist(request):
    watchlist = []
    curr_user = request.user
    for listing in Listing.objects.all():
        if curr_user in listing.watchlist.all():
            watchlist.append(listing)
    return render(request, "auctions/show_watchlist.html", {
        "watchlist": watchlist
    })

def post_comment(request, listing_id):
    if request.method == "POST":
        commentor = request.user
        listing = Listing.objects.get(pk=listing_id)
        message = request.POST['message']

        # create comment
        new_comment = Comment(
            commentor = commentor,
            listing = listing,
            message = message,
        )
        # save data
        new_comment.save()
        # redirect !! doesn't use httpresponse redirect (?)
        return HttpResponseRedirect(reverse("listing", args=(listing.title, )))

def list_categories(request):
    return render(request, "auctions/categories.html", {
        "categories":Category.objects.all()
    })

def category_listing(request, category):
    category = Category.objects.get(cat_name=category)
    listings = []
    for listing in Listing.objects.all():
        if listing.category == category:
            listings.append(listing)
    return render(request, "auctions/category_listings.html", {
        "category":category,
        "listings":listings
    })




    




