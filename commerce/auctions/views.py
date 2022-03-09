from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm


from .models import Bid, User, Listing, Category, Comment


class CreateNewListing(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "current_price", "picture", "picture_text", "category"]


class CreateNewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ["text_comment"]


class CreateBid(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]


def index(request):
    """This function renders the index page and provides the listings database"""
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    """When a user tries to GET the page, this view renders a login form.
    When a form is sumbitted using POST, the user
    is authenticated, signed in, and brought to the home page."""
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
    """This view logs out the user and then returns to the index page"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """This view renders a registration form, and creates a new user
    when the form is submitted. """
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
    """This view renders the create listing form. If the request method
     is POST the sumbited data is saved to the listing database and the user
     is redirected to the index page."""
    if request.method == "POST":
        form = CreateNewListing(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user   # The user is included as the seller
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    form = CreateNewListing()
    return render(request, "auctions/create_listing.html", {
        "form": form,
    })


def listing_page(request, listing_id):
    """This view renders a page for each auction listing"""
    # retrieves listing by id
    listing_page = Listing.objects.get(id=listing_id)
    form = CreateNewComment()
    bid_form = CreateBid()

    # sets the starting bid as the first bid object
    
    if listing_page.bids.all():
        pass
    else:
        starter_bid = Bid(amount = listing_page.current_price, listing = listing_page, bidder = request.user )
        starter_bid.save()
    last_bids = listing_page.bids.last()


    # reference for including multiple forms in a view:
    # https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form
    if request.method == "POST" and 'create_comment' in request.POST:
        form = CreateNewComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # includes addition data to save comment
            comment.author = request.user      
            comment.listing = listing_page
            comment.save()
            return HttpResponseRedirect(reverse("listing_page", kwargs={"listing_id": listing_id}))

    if request.method == "POST" and 'add_watchlist' in request.POST:
        # adds the listing to the user's watchlist
        listing_page.watchers.add(request.user)
        listing_page.save()

    if request.method == "POST" and 'remove_watchlist' in request.POST:
        # removes the listing to the user's watchlist
        current_user = request.user
        current_user.watching.remove(listing_page)

    if request.method == "POST" and 'place_bid' in request.POST:
        form = CreateBid(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            # includes additional data to save comment
            new_bid.bidder = request.user      
            new_bid.listing = listing_page
            new_bid.save()
            return HttpResponseRedirect(reverse("listing_page", kwargs={"listing_id": listing_id}))
    
    if request.method == "POST" and 'close_page' in request.POST:
        # removes the listing to the user's watchlist
        listing_page.closed = True
        listing_page.save()

    return render(request, "auctions/listing_page.html", {
        "current_user": request.user,
        "watchers": listing_page.watchers.all(),
        "form": form,
        "bid_form": bid_form,
        "listing": listing_page,
        "comment": listing_page.comments.all(),
        "last_bids": last_bids,
        # the last bid is used to set a minimum value required in the CreateBid Field
        "lower_bound": round((float(last_bids.amount) + (0.01)), 2)
    })


def category_page(request):
    """This view renders a page that displays links 
    for different item categories"""
    categories = Category.objects.all()
    return render(request, "auctions/category_page.html", {
        "categories": categories,
    })


def category_contents(request, category_id):
    """This view renders the pages for items within a category, and provides
    the page with all the listings in a given category"""
    category_content = Category.objects.get(id=category_id)   
    category_listings = category_content.listings.all()
    return render(request, "auctions/category_contents.html", {
        "category_content": category_content,
        "category_listings": category_listings
    })


def watchlist(request):
    """This view renders a page where users can see what items are on their
    watchlist"""
    current_user = User.objects.get(username=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": current_user.watching.all()
    })
