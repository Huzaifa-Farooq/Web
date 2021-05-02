from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max

from .models import User, AuctionListing, AuctionBids, Watchlist, Comments

items_categories = ["Fashion", "Toy", "Home", "Electronics", "Health & Beauty", "Home Appliances", "Sports & Outdoor", "Education"]

def index(request):

    # getting active listings query
    query = AuctionListing.objects.exclude(is_active=False)

    # getting active listing ids as a list
    active_auction_list = list(query.values_list('id', flat=True))

    max_bid_dict = {}
    for active_auction_id in active_auction_list:
        query_set = AuctionBids.objects.filter(listingid=active_auction_id)
        highest_bid = query_set.aggregate(Max('current_bid'))['current_bid__max']
        if highest_bid is None:
            highest_bid = AuctionListing.objects.get(pk=active_auction_id).starting_bid
        max_bid_dict[int(active_auction_id)] = highest_bid


    return render(request, 'auctions/index.html', {
        'auctions': AuctionListing.objects.filter(pk__in=active_auction_list),
        "max_bids": max_bid_dict

        ###     solving current bid in index issue
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
        return render(request, "auctions/login.html", {"no_of_items": 55})


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
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        url = request.POST["url"]
        category = request.POST["category"]
        created_by = User.objects.get(username=request.user.username)


        AuctionListing(title=title, created_by=created_by, starting_bid=starting_bid,
                       description=description, url=url, category=category).save()

        last_listing_id = AuctionListing.objects.all().last()

        user = User.objects.get(listings=last_listing_id.id)

        AuctionBids(listingid=last_listing_id, user=user, current_bid=starting_bid).save()
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "auctions/create_listing.html", {
            "categories": items_categories
        })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": items_categories
    })


def listing_categories(request, category):

    auctions = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/listing_categories.html", {
        "auctions": auctions,
        "category": category
    })


@login_required(login_url="/login")
def make_bid(request, listing_id):
    bid_warning = False
    listing = AuctionListing.objects.get(pk=listing_id)
    query_list = []

    for query in Watchlist.objects.filter(user=request.user):
        query_list.append(query.listing_id)

    if listing_id in query_list:
        can_add_to_watchlist = False
    else:
        can_add_to_watchlist = True

    bid_made = request.POST["bid"]
    # if there is not bid
    try:
    # query to select last bid made
        last_bid_made = AuctionBids.objects.filter(listingid=listing_id).last().current_bid
        if int(last_bid_made) == 0:
            last_bid_made = AuctionListing.objects.filter(pk=listing_id).starting_bid

    except AttributeError:
        last_bid_made = 0

    username = request.user.username

    user = User.objects.get(username=username)

    listing_id = AuctionListing.objects.get(pk=listing_id)

    no_of_bids = len(list(AuctionBids.objects.filter(listingid=listing_id))) - 1


    if request.method == "POST":
        # warning if bid is less

        if int(bid_made) > int(last_bid_made) and int(bid_made) > int(AuctionListing.objects.filter(id=listing_id.id)[0].starting_bid):
            AuctionBids(user=user, listingid=listing_id, current_bid=bid_made).save()
            AuctionListing.objects.filter(id=listing_id.id).update(starting_bid=bid_made)
            return redirect(f"/{listing_id.id}/listings")

        else:
            bid_warning = True
            return render(request, 'auctions/listings.html', {
                "listing": listing,
                "no_of_bids": no_of_bids,
                "can_add_to_watchlist": can_add_to_watchlist,
                "bid_warning": bid_warning,
                "last_bid": last_bid_made
            })

    else:
        return render(request, 'auctions/listings.html', {
            "listing": listing,
            "no_of_bids": no_of_bids,
            "can_add_to_watchlist": can_add_to_watchlist,
            "bid_warning": bid_warning,
            "last_bid": last_bid_made
        })


def listings(request, listing_id):
    # warning if bid is less
    bid_warning = False

    user = User.objects.get(username=request.user.username)
    query_list = Watchlist.objects.filter(user=user).values_list('listing_id', flat=True)

    listing = AuctionListing.objects.get(pk=listing_id)

    if listing_id in query_list:
        can_add_to_watchlist = False
    else:
        can_add_to_watchlist = True

    comments = Comments.objects.filter(listing_id=listing_id)

    # selecting the user who has won the bid if it is closed
    query = AuctionBids.objects.filter(listingid=listing_id)
    highest_bid = query.aggregate(Max('current_bid'))
    won_by = AuctionBids.objects.filter(current_bid=highest_bid['current_bid__max']).last()

    if str(listing.created_by) == request.user.username:
        show_buttons = True
    elif str(listing.created_by) != request.user.username:
        show_buttons = False
    print(f"\n\n\n\n\n{listing.created_by} {request.user.username}")


    if request.method == "GET":
        query = AuctionBids.objects.filter(listingid=listing_id)
        highest_bid = query.aggregate(Max('current_bid'))
        return render(request, 'auctions/listings.html', {
            "listing": listing,
            "show_buttons": show_buttons,
            "current_bid": highest_bid['current_bid__max'],
            "no_of_bids": len(list(AuctionBids.objects.filter(listingid=listing_id))),
            "can_add_to_watchlist": can_add_to_watchlist,
            "bid_warning": bid_warning,
            "comments": comments,
            "highest_bid": highest_bid['current_bid__max'],
            "won_by": won_by
        })


@login_required(login_url="/login")
def show_watchlist(request, user):
    user = User.objects.get(username=user)
    # returns filtered query
    query = Watchlist.objects.filter(user=user)

    # get watchlist listing ids
    watchlist_listing_ids = list(query.values_list('listing_id', flat=True))
    watchlist = AuctionListing.objects.filter(pk__in=watchlist_listing_ids)
    return render(request, "auctions/show_watchlist.html", {
        "auctions": watchlist
    })



@login_required(login_url="/login")
def close_auction(request, listing_id):
    if request.method == "POST":
        AuctionListing.objects.filter(pk=listing_id).update(is_active=False)
        return redirect(f"/{listing_id}/listings")
    else:
        return redirect(f"/{listing_id}/listings")


@login_required(login_url="/login")
def delete_listing(request, listing_id):
    if request.method == "POST":
        AuctionListing.objects.filter(pk=listing_id).delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return redirect(f"/{listing_id}/listings")


@login_required(login_url="/login")
def user_auctions(request, user):
    user = User.objects.get(username=user)

    active_auctions = AuctionListing.objects.filter(created_by=user, is_active=True)

    closed_auctions = AuctionListing.objects.filter(created_by=user, is_active=False)

    return render(request, "auctions/user_auctions.html", {
        "active_auctions": active_auctions,
        "closed_Auctions": closed_auctions,
        "created_by": user
    })


@login_required(login_url="/login")
def make_comment(request, listing_id):
    listing_id = AuctionListing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        comment = request.POST["comment"]
        Comments(listing_id=listing_id, comment=comment, user=user).save()
        return redirect(f"/{listing_id.id}/listings")
    else:
        return redirect(f"{listing_id.id}/listings")


@login_required(login_url="/login")
def remove_from_watchlist(request, listing_id):

    username = request.user.username
    user = User.objects.get(username=username)
    listing_id = AuctionListing.objects.get(pk=listing_id)

    if request.method == "POST":
        Watchlist.objects.filter(user=user, listing_id=listing_id).delete()
        return HttpResponseRedirect(reverse('listings', args=[listing_id.id]))
    else:
        # user came through a redirect
        return HttpResponseRedirect(reverse('listings', args=[listing_id.id]))


@login_required(login_url="/login")
def add_to_watchlist(request, listing_id):
    username = request.user.username
    user = User.objects.get(username=username)
    listing_id = AuctionListing.objects.get(pk=listing_id)

    if request.method == "POST":
        Watchlist(user=user, listing_id=listing_id).save()
        return HttpResponseRedirect(reverse('listings', args=[listing_id.id]))
    else:
        return HttpResponseRedirect(reverse('listings', args=list(listing_id.id)))