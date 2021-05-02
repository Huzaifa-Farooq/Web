from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("users/<str:user>/listings", views.user_auctions, name="user_auctions"),
    path("users/<str:user>/watchlist", views.show_watchlist, name="show_watchlist"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.listing_categories, name="listing_categories"),
    path('create_listing', views.create_listing, name="create_listing"),
    path('<int:listing_id>/listings', views.listings, name="listings"),
    path('<int:listing_id>/listings/close', views.close_auction, name="close_auction"),
    path('<int:listing_id>/listings/bid', views.make_bid, name="make_bid"),
    path('<int:listing_id>/listings/remove', views.remove_from_watchlist, name="remove_from_watchlist"),
    path('<int:listing_id>/listings/add', views.add_to_watchlist, name="add_to_watchlist"),
    path('<int:listing_id>/listings/comment', views.make_comment, name="make_comment"),
    path('<int:listing_id>/listings/delete', views.delete_listing, name="delete_listing"),
]
