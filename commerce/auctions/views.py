from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, auction_listing, comments, bid, Category


def index(request):
    return render(request, "auctions/index.html", {
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
    
def listing_view(request):
    listings = auction_listing.objects.all()
    print(f"DEBUG: Found {listings.count()} listings in DB")
    listing_data = {}
    for listing in listings:
        listing_data[listing] = listing.comments.all()
        listing.bid_count = listing.bids.count()
    return render(request, "auctions/index.html",{
        "auction_listings": listings,
        "listing_data": listing_data
    
    })
@login_required
def add_bid(request, listing_id):
    if request.method == "POST":
        listing = auction_listing.objects.get(id=listing_id)
        bid_value = request.POST.get("bid_amount")
        if not bid_value:
            messages.error(request,"Please enter a bid amount.")
        new_bid_amount = float(request.POST["bid_amount"])
        
        if new_bid_amount > listing.price:
            new_bid = bid(
                amount = new_bid_amount,
                user = request.user,
                auction_listing=listing
            )
            new_bid.save()
            
            listing.price = new_bid_amount
            listing.save()
            
            messages.success(request, "Bid placed successfully!")
        else:
            messages.error(request, "Your bid shoul be higher than current price.")
    return redirect("index")   
@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        listing = auction_listing.objects.get(id=listing_id)
        comment_text = request.POST.get("comment_text")
        
        if comment_text:
            new_comment = comments(
                message=comment_text,
                user=request.user,
                auction_listing=listing
            )
            new_comment.save()
            messages.success(request, "Comment added!")
        else:
            messages.error(request, "Comment not successful.")
            
    return redirect("index")
@login_required
def add_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to create a new listing.")
        return redirect("login")
    if request.method =="POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        image = request.POST.get("image_url")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        
        
        new_listing = auction_listing(
            name=name,
            price=price,
            image_url=image,
            user=request.user,
            active=True,
            owner=request.user,
            category=category
        )
        new_listing.save()
        
        messages.success(request, f"Successfully added {name}!")
        return redirect("index")
    
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })
@login_required   
def delete_listing(request, listing_id):
    listing = get_object_or_404(auction_listing, id=listing_id)
    
    if request.user == listing.owner:
        listing.delete()
        return redirect("index")
    else:
        return redirect("listing_detail", listing_id=listing.id)
   
def details(request, listing_id):
    listing = auction_listing.objects.get(id=listing_id)
    
    return render(request,"auctions/listing.html", {
        "listing": listing,
    })                   
@login_required   
def toggle_watchlist(request, listing_id):
    listing = auction_listing.objects.get(id=listing_id)
    if listing.watchlist.filter(id=request.user.id).exists():
        listing.watchlist.remove(request.user)
        messages.success(request, f"{listing.name} removed from watchlist.")
        
    else:
        listing.watchlist.add(request.user)
        messages.success(request, f"{listing.name} added to watchlist.")
        
    return redirect("listing_details", listing_id=listing_id)

@login_required
def watchlist_view(request):
    watched_items = request.user.watched_list.all()
    return render(request, "auctions/watchlist.html", {
        "listings": watched_items
    })
def categories(request):
    return render(request, "auctions/layout.html", {
        "categories": Category.objects.all()
    })   
def category_filter(request, category_id):
    all_categories = Category.objects.all()
    category = Category.objects.get(id=category_id)
    listings = auction_listing.objects.filter(category=category, active=True)
    return render(request, "auctions/index.html", {
        "all_categories": all_categories,
        "auction_listings": listings,
        #"category_name": category.name
    })