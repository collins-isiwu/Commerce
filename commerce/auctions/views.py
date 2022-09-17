from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import NewListingForm, CommentForm, BidForm
from .models import User, Listing, Category, Bids
from django.contrib import messages


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True),
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
    if request.method == 'POST':

        # Take in the data the user submitted and save it as form
        form = NewListingForm(request.POST)

        # Checks if the form data is valid
        if form.is_valid():
            # Sets creator field 
            form.instance.creator = request.user
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


def listing(request, listing_id):

    # Look up the relevant information from the db to load the page
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all()
    totalComments = comments.count()

    # checks if the user is on the watchlist of the listing
    if request.user.is_authenticated:
        is_in_watchlist = listing.is_in_watchlist(request.user)
    else:
        is_in_watchlist = False

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "listing_id": listing_id,
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


# Shows all the listings under a category
def category(request, category_id):
    return render(request, "auctions/category.html", {
        "category": Category.objects.get(pk=category_id),
        "listings": Listing.objects.filter(active=True, category=category_id) 
    })


@login_required(login_url='login')
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })


@login_required(login_url='login')
def removewatchlist(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)

        listing.watched_by.remove(user)

        # success message
        messages.success(request, "Action successful!")
        return HttpResponseRedirect(reverse('watchlist'))



@login_required(login_url='login')
def ChangeWatchlist(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)

        # Removes the listing from watchlist if it is already there
        if listing.is_in_watchlist(user):
            listing.watched_by.remove(user)
        else:
            listing.watched_by.add(user)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url='login')
def addbid(request, listing_id):
    if request.method == "POST":

        # obtain the listing id
        listing = Listing.objects.get(pk=listing_id)

        # save the users input in the form variable
        form = BidForm(request.POST)

        # check if the form data is valid
        if form.is_valid():
            
            # Set the user and item fields in their respective Models
            form.instance.user = request.user
            form.instance.item = listing

            # bid must be higher than the starting bid and current(highest) bids 
            if form.instance.amount < listing.highest_bid():
                
                messages.error(request, "Your bid should be higher than the current bid.")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

            else:
                
                # save the bid from BidForm to the database
                form.save()

                # Success message
                messages.success(request, "Bid successful!")

    # Reloads page
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url='login')
def closebid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST' and listing.creator == request.user:
        
        # Closes auction for the creator by updating the databse
        Listing.objects.filter(pk=listing_id).update(active=False)

        # Success message
        messages.success(request, "Auction Successfully Closed!")
        return redirect('/')

    else:
        return render (request, "auctions/error.html", {
            "message": "You are not Authorised to do this!"
        })


@login_required(login_url='login')
def addcomment(request, listing_id):
    if request.method == "POST":
        # Gets the listing id of the listed product
        listing = Listing.objects.get(pk=listing_id)

        # save the users input in the variable form
        form = CommentForm(request.POST)

        # validate the form
        if form.is_valid:
            form.instance.user = request.user
            form.instance.listing = listing

            # saves comment to database
            form.save()

            # Success message
            messages.success(request, "Comment Successfully Added!")

            # Reload page
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))