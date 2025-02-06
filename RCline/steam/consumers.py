import json
import httpx  # Используем асинхронный клиент
from bs4 import BeautifulSoup as bs
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.fetch_games(5)  # Загружаем 5 страниц

    async def fetch_games(self, max_pages):
        base_url = "https://store.steampowered.com/search/?specials=1&page="

        async with httpx.AsyncClient() as client:
            for page in range(1, max_pages + 1):
                try:
                    response = await client.get(f"{base_url}{page}")
                    response.raise_for_status()  # Проверка HTTP-ошибок

                    soup = bs(response.text, 'html.parser')
                    games = soup.find_all("span", class_="title")
                    game_prices = soup.find_all("div", class_="discount_final_price")
                    games_full_prices = soup.find_all("div", class_="discount_original_price")
                    games_percents = soup.find_all("div", class_="discount_pct")
                    games_url = soup.find_all("a", class_="search_result_row")

                    if not games:
                        break

                    page_games = []

                    for i in range(len(games)):
                        games_img = games_url[i].find("img") if i < len(games_url) else None
                        page_games.append({
                            "title": games[i].text if i < len(games) else "N/A",
                            "price": game_prices[i].text if i < len(game_prices) else "N/A",
                            "full_price": games_full_prices[i].text if i < len(games_full_prices) else "N/A",
                            "percent": games_percents[i].text if i < len(games_percents) else "N/A",
                            "url": games_url[i].get('href') if i < len(games_url) else "N/A",
                            "img": games_img.get('src') if games_img else "N/A",
                        })

                    # Отправляем данные на фронтенд
                    await self.send(text_data=json.dumps({"games": page_games, "page": page}))

                except httpx.RequestError as e:
                    await self.send(text_data=json.dumps({"error": str(e)}))
                    await self.close()
                    break

    async def disconnect(self, close_code):
        print(f"WebSocket отключен: {close_code}")
