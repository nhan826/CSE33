from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm


from .models import User, Listing


class CreateNewListing(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "current_price", "picture", "picture_text", "category" ]


def index(request):
    """This function renders the index page and provides the listings database """
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
    listing_page = Listing.objects.get(id = listing_id)    # retrieves listing by id
    return render(request, "auctions/listing_page.html", {
        "listing": listing_page,   
    })
    