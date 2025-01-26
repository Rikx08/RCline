from django.urls import path
from . import views
urlpatterns = [
   # path("", views.index, name="steam"),
   path("", views.steam_sales),

]
