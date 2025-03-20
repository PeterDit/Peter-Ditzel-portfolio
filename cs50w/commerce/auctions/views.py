from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import ListingForm
from django.contrib.auth.decorators import login_required
from flask import Flask, flash 
from .models import User, Listing, watchlistmodel, Category, Bid, Member
from django.template import loader


# Index page
def index(request):
    return render(request, "auctions/index.html")

# Login user
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

# Logout user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Registers a user account
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

@login_required(login_url="login")
# View to handle the creation of a new listing
def create_listing(request):
    if request.method == "POST":
        # Create a form instance with POST data
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database (ListingForm is linked to the Listing model)
            form.instance
            form.instance.creator = request.user
            form.save()
            # Redirect to a page of your choice after saving 
            return redirect('index')
    else: 
        # Create an empty form instance
        form = ListingForm()  
        # Render the form in the template
    return render(request, 'auctions/listing.html', {'form': form})

# Lists all listed auctions
def active_listings(request):
    listings = Listing.objects.all()  # You can filter based on your criteria for "active"
    highest_bids = {
        }
    for listing in listings:
        highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
        highest_bids[listing] = highest_bid
        
    return render(request, 'auctions/active_listings.html', {'listings': listings, 'highest_bid':highest_bid })

# Removes listing from the list
@login_required(login_url="login")
def remove_listings(request, listing):
    if request.method == "POST":
        # Get the listing ID from the form data
        listing_id = request.POST.get('listing_id')

        # Retrieve the listing object from the database
        listing = Listing.objects.get(pk=listing_id)

        # Check if current user logged in has any listings
        if listing.creator == request.user:
                
            # Delete the listing
            listing.delete()

            # Redirect to a page of your choice after deleting
            return redirect('index')  # Replace 'index' with the appropriate URL name
            
        else:
            messages.error(request,'Not your listing')
            return redirect('active_listings')
        
# To create category
def category(request):
    listings = Listing.objects.all()
        
# Adds item to a watchlist
@login_required(login_url="login")
def add_watchlist(request, listing_id):
    items = Listing.objects.get(pk=listing_id)
    watched = watchlistmodel.objects.filter(user=request.user, item=listing_id)
    if request.method == 'POST':
        if watched.exists():
            watched.delete()
            messages.success(request, 'Listing removed from watchlist')
            # messages.add_message(request, messages.ERROR, "Successfully deleted from your watchlist")
            return HttpResponseRedirect(reverse("watchlist"))
            
        else:
            watched, created = watchlistmodel.objects.get_or_create(user=request.user)
            watched.item.add(items)
            # messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
            return redirect('watchlist')
    else:
        return HttpResponseRedirect(reverse("watchlist")) 

# Filter watchlist items by logged in user, and pass to template
@login_required(login_url="login")
def watchlist(request):
    watchlists = watchlistmodel.objects.filter(user=request.user)
    context = {'watchlists':watchlists}
    watchlistmodel.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', context)

# Removes item from watchlists
@login_required(login_url="login")
def remove_watchlist(request, listing_id):
    if watchlistmodel.objects.filter(user=request.user, item=listing_id).exists():
        watchlists = watchlistmodel.objects.get(user=request.user, item=listing_id)
        watchlists.item.remove(listing_id)
        return HttpResponseRedirect(reverse("watchlist"))    
    else:
        return HttpResponseRedirect(reverse("watchlist"))

# To display the comments + names on the website
@login_required(login_url="login")
def members(request):
    print("Hi")
    mymembers = Member.objects.all().values()
    template = loader.get_template('auctions/listing_detail.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))

# Get specific listing by id
def listing_detail(request, listing_id):
    mymembers = Member.objects.all().values()
    template = loader.get_template('auctions/listing_detail.html')
    context = {
        'mymembers': mymembers,
    }
    if request.method == "POST":
        x = request.POST['firstname']
        y = request.POST['lastname']
        z = request.POST['comment']       
        listings = Listing.objects.get(pk=listing_id)
        mymembers = Member.objects.filter(listing=listings)
        newmembers = Member(firstname = x, lastname = y, comment = z, listing=listings)
        newmembers.save()
        return render(request, "auctions/listing_detail.html", {"listing": listings, "mymembers":mymembers, "listing_id": listing_id})
    else:
        if request.method == "GET":
            listings = Listing.objects.get(pk=listing_id)
            template = loader.get_template('auctions/listing_detail.html')
            mymembers = Member.objects.filter(listing=listings)
            return render(request, "auctions/listing_detail.html", {"listing": listings, "mymembers":mymembers, "listing_id": listing_id})     

# Getting al categories and pass to template
def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories":all_categories})

# Get specific category by its id and filter by
def category(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Listing.objects.filter(category=category)
    print(categories)
    return render(request, "auctions/categories.html", {"categories": categories, "listings": listings})

# Lets the user bid on the auction
@login_required(login_url="login")
def bid(request, listing_id):
    # Holds a specific listing object (using its id)
    listings = Listing.objects.get(pk=listing_id)
    # Takes the bid amount via post, if amount is missing, it uses the starting bid. Converts it then to a float
    new_bid = float(request.POST.get('amount', listings.starting_bid))
    highest_bid = Bid.objects.filter(listing=listings).order_by('-amount').first()
    # Starting bid
    starting_bid = listings.starting_bid  
    listings.updated_bid = listings.starting_bid
    if listings.is_active is False:
            messages.error(request,"This auction has endet.")
            # If bid is to low
    else:
        if new_bid <= starting_bid or new_bid <= highest_bid.amount:
            messages.error(request, "Needs to be higher than current bid.")
            return render(request, 'auctions/active_listings.html', {})
        else: 
            # Create a new bid object, saving and displaying it 
            new_bid = Bid(amount=new_bid, listing=listings, user=request.user)
            new_bid.save()
            listings.updated_bid = new_bid.amount
            listings.save()
            messages.success(request, "Congratulations, you bid ${} on this item. ".format(new_bid.amount))
            return render(request, 'auctions/active_listings.html', {})
    
# Calculate the endtime of a auction
def endtime(request, listing_id):
    duration_to_hours = {
        "1 Day": 24,
        "2 Days": 48,
        "5 Days": 120,
        "10 Days": 240
    }
    # Gets duration time
    duration_time = request.POST['duration']
    # Sets it to the hours from the list above
    hours = duration_to_hours[duration_time] 
    # Get Listing
    listings = Listing.objects.get(pk=listing_id)
    # Get Bid
    highest_bid = Bid.objects.filter(listing=listings).order_by('-amount').first()
    created_at = listings.created_at
    current_time = timezone.now()
    # Creating the end_time
    end_time = created_at + timedelta(hours=hours)
    if listings.is_active is True:
        # Compares end_time to current time, if condition true it prints out winner
        if end_time < current_time:
            print("Congratulations", highest_bid.user, "You won the auction")
            listings.is_active = False
            listings.save()