from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"), 
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addcomment/<int:listing_id>", views.addcomment, name="add_comment"),
    path("removewatchlist//<int:listing_id>", views.removewatchlist, name="remove_watchlist"),
    path("changewatchlist/<int:listing_id>", views.ChangeWatchlist, name="change_watchlist"),
    path("closebid/<int:listing_id>", views.closebid, name="closebid"),
    path("addbid/<int:listing_id>", views.addbid, name="add_bid")
]
