import requests
from bs4 import BeautifulSoup as bs

base_url = "https://store.steampowered.com/search/?specials=1&page="

def fetch_games(max_pages):
    all_games = []

    for page in range(1, max_pages + 1):  # Перебираем страницы
        url = f"{base_url}{page}"
        r = requests.get(url)

        if r.status_code == 200:  # Парсим данные
            soup = bs(r.text, 'html.parser')
            games = soup.find_all("span", attrs={"class": "title"})
            game_prices = soup.find_all("div", attrs={"class": "discount_final_price"})
            games_full_prices = soup.find_all("div", attrs={"class": "discount_original_price"})
            games_percents = soup.find_all("div", attrs={"class": "discount_pct"})

            if not games:
                print(f"На странице {page} игр больше нет.")
                break

            for i in range(len(games)):  # Собираем данные в один объект
                all_games.append({
                    "title": games[i].text if i < len(games) else "N/A",
                    "price": game_prices[i].text if i < len(game_prices) else "N/A",
                    "full_price": games_full_prices[i].text if i < len(games_full_prices) else "N/A",
                    "percent": games_percents[i].text if i < len(games_percents) else "N/A"
                })

            print(f"Страница {page}: собрано {len(games)} игр.")
        else:
            print(f"Ошибка запроса на странице {page}: {r.status_code}")
            break

    return all_games
