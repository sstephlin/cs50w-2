from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"), 
    path("listing/<str:listing_title>", views.listing, name="listing"),
    path("bid/<int:listing_id>", views.place_bid, name="place_bid"), 
    path("add_watch/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watch/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"), 
    path("show_watchlist", views.show_watchlist, name="show_watchlist"),
    path("post_comment/<int:listing_id>", views.post_comment, name="post_comment"),
    path("categories", views.list_categories, name="list_categories"),
    path("category_listing/<str:category>", views.category_listing, name="category_listing")
]
