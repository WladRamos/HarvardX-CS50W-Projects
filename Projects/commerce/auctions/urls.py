from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
    path("make_bid/<int:listing_id>/", views.make_bid, name='make_bid'),
    path("close_auction/<int:listing_id>/", views.close_auction, name="close_auction"),
    path("comments/<int:listing_id>/", views.comments, name="comments"),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.category_listings, name='category_listings'),
]
