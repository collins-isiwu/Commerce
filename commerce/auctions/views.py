from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import NewListingForm, CommentForm, BidForm
from .models import User, Listing, Category


def index(request):
    return render(request, "auctions/index.html", {
        "Listing": Listing.objects.all()
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

@login_required(login_url='login')
def createlisting(request):
    if request == 'POST':

        # Take in the data the user submitted and save it as form
        form = NewListingForm(request.POST)

        # Checks if the form data is valid
        if form.is_valid():
            # Sets creator field 
            form.instance.author = request.user
            # Saves new listing
            new_listing = form.save()
            # Redirect the user to listing page
            return HttpResponseRedirect(reverse("listing", args=(new_listing.pk,)))
    else:
        # If the user request via GET (or any other method), we'll create a blank form
        form = NewListingForm()

        return render (request, "auctions/newlisting.html", {
            "form": form
        })


def listing(request, Listing_id):

    # Look up the relevant information from the db to load the page
    listing = Listing.objects.get(pk=Listing_id)
    comments = listing.comments.all()
    totalComments = comments.count()

    # checks if the user is on the watchlist of the listing
    if request.user.is_authenticated:
        is_in_watchlist = listing.is_in_watchlist(request.user)
    else:
        is_in_watchlist = False

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "listing_id": Listing_id,
        "comments": comments, 
        "totalComments": totalComments,
        "is_in_watchlist": is_in_watchlist, 
        "user": request.user,
        "Bidform": BidForm(),
        "comment_form": CommentForm()
    })


# Page that shows lists of categories available on the website
def categories(request):
    return render (request, "auctions/categories.html", {
        "categories": Category.objects.all().order_by('categorified')
    })


# Shows all the listing under a category
def category(request, category_id):
    return render(request, "auctions/category.html", {
        "category": Category.objects.get(pk=category_id),
        "listings": Listing.objects.filter(active=True, category=category_id) 
    })


def watchlist(request):
    pass

