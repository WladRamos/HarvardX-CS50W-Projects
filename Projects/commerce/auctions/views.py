from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Category, Listing, Watchlist, Bid, Comment, User
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        img_url = request.POST["img_url"]

        new_listing = Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            greater_bid=0,
            owner=request.user,
            url = img_url
        )
        new_listing.save()
        active_listings = Listing.objects.filter(status=True)
        return render(request, "auctions/index.html", {
            "listings": active_listings
        })
    active_listings = Listing.objects.filter(status=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })

def closed_listings(request):
    closed = Listing.objects.filter(status=False)
    return render(request, "auctions/closed_listings.html", {
        "listings": closed
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

@login_required
def new_listing(request):
    return render(request, "auctions/new_listing.html", {
        "categories": Category.objects.all()
    })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    price_type = ""
    price = 0

    if listing.starting_bid > listing.greater_bid:
        price = listing.starting_bid
        price_type = "Starting bid"
    else:
        price = listing.greater_bid
        price_type = "Greater bid"
    
    is_in_watchlist = request.user.is_authenticated and request.user.watchlist_set.filter(listing=listing).exists()

    is_owner = request.user.is_authenticated and listing.owner == request.user

    is_winner = request.user.is_authenticated and listing.winner == request.user and not listing.status

    comments = Comment.objects.filter(listing=listing)

    return render(request, "auctions\listing.html", {
        "listing": listing,
        "price_type": price_type,
        "price": price,
        "categories": listing.category.all(),
        "is_in_watchlist": is_in_watchlist,
        "is_owner": is_owner,
        "is_winner": is_winner,
        "comments": comments,
    })

@login_required
def watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    
    if Watchlist.objects.filter(user=user, listing=listing).exists():
        Watchlist.objects.filter(user=user, listing=listing).delete()
    else:
        new_watching_item = Watchlist.objects.create(
            user=user,
            listing=listing
        )
        new_watching_item.save()

    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

@login_required
def watchlist_page(request):
    watchlist_listings = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {"watchlist_listings": watchlist_listings})


@login_required
def make_bid(request, listing_id):
    if request.method == 'POST':
        bid_value = int(request.POST.get('bid_value'))
        listing = Listing.objects.get(pk=listing_id)
        
        if listing.starting_bid > listing.greater_bid:
            minimum_bid = listing.starting_bid
        else:
            minimum_bid = listing.greater_bid
        
        if bid_value >= minimum_bid:
            bid = Bid.objects.create(listing=listing, author=request.user, value=bid_value)
            listing.greater_bid = bid_value
            listing.save()
            bid.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))

@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST' and listing.owner == request.user:
        if listing.greater_bid != 0:
            highest_bid = listing.bids.get(value=listing.greater_bid)
            if highest_bid:
                listing.winner = highest_bid.author
        listing.status = False
        listing.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

@login_required
def comments(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        comment = request.POST.get('comment')
        if comment:
            new_comment = Comment.objects.create(author=request.user, listing=listing, comment=comment)
            new_comment.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})

def category_listings(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category, status=True)
    return render(request, "auctions/category_listings.html", {"category": category, "listings": listings})
