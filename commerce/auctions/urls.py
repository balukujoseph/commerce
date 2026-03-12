from django.urls import path

from . import views

urlpatterns = [
    path("", views.listing_view, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("create", views.add_listing, name="add_listing"),
    path("listing/<int:listing_id>", views.details, name="listing_details"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("toggle_watchlist/<int:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_filter, name="category_filter"),
    path("category/<int:category_id>", views.category_filter, name="category_filter"),
    path("delete/<int:listing_id>", views.delete_listing, name="delete_listing")
]
