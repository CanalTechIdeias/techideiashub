from django.urls import path, include

from . import views


urlpatterns = [
    path("sign_up/", views.sign_up, name="sign_up"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile/<slug:slug>/", views.public_profile, name="public_profile"),
    path("profile/<slug:slug>/update/", views.update_profile, name="update_profile"),
    path("profile/<slug:slug>/delete/", views.delete_profile, name="delete_profile"),
]