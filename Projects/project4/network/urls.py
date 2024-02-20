
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("api/follow/<user_id>/", views.follow_unfollow_user, name='follow_unfollow_user'),
    path("api/edit/<post_id>", views.edit_post, name="edit_post")
    
]
