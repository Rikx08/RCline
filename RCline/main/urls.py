from django.urls import path, include

from . import views

urlpatterns = [
   path("", views.index, name="load_main_page"),
   path("profile", include("registrations.urls")),
   path("accounts/", include("django.contrib.auth.urls")),
]
