from django.urls import include, path
from django.contrib import admin
from auctions import views
from django.conf.urls.static import static
from django.conf import settings

# Loading the function to the site
urlpatterns = [ 
    path("index", views.index, name="index"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("active/", views.active_listings, name="active_listings"),
    path("remove/<int:listing>/", views.remove_listings, name="remove_listings"),
    path("add_watchlist/<int:listing_id>/", views.add_watchlist, name="add_watchlist"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<int:category_id>/", views.category, name="category_id"),
    path("listing_detail/<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("bid/<int:listing_id>/", views.bid, name="bid"),
    path('listing_detail/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)