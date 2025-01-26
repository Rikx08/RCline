from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
from .parser import fetch_games

# def index(request):
#     return render(request, "steam/steam.html")


def steam_sales(request):
    max_pages_to_fetch = 10  # Количество страниц для парсинга
    games = fetch_games(max_pages_to_fetch)  # Получаем список игр
    return render(request, "steam/steam.html", {'games': games})