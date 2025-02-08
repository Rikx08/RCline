import json
import asyncio
import httpx
from bs4 import BeautifulSoup as bs
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.page = 1
        self.keep_alive = True
        print("WebSocket подключен")

    async def receive(self, text_data):
        """Обрабатываем входящие запросы"""
        data = json.loads(text_data)
        if data.get("action") == "load_games":
            page = data.get("page", 1)
            await self.fetch_games(page)

    async def fetch_games(self, page):
        """Загружаем и отправляем игры с указанной страницы"""
        base_url = "https://store.steampowered.com/search/?specials=1&page="

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{base_url}{page}")
                response.raise_for_status()

                soup = bs(response.text, 'html.parser')
                games = soup.find_all("span", class_="title")
                game_prices = soup.find_all("div", class_="discount_final_price")
                games_full_prices = soup.find_all("div", class_="discount_original_price")
                games_percents = soup.find_all("div", class_="discount_pct")
                games_url = soup.find_all("a", class_="search_result_row")

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

                await self.send(text_data=json.dumps({"games": page_games, "page": page}))

            except httpx.RequestError as e:
                await self.send(text_data=json.dumps({"error": str(e)}))

    async def disconnect(self, close_code):
        """Отключение WebSocket-соединения"""
        self.keep_alive = False
        print(f"WebSocket отключен: {close_code}")
