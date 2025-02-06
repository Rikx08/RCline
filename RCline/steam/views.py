from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
# from .parser import
#
# # def index(request):
# #     return render(request, "steam/steam.html")
#
#
def steam_sales(request):
    return render(request, "steam/steam.html")