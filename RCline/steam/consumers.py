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
        base_url = f"https://store.steampowered.com/search/?specials=1&page={page}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(base_url)
                response.raise_for_status()

                soup = bs(response.text, 'html.parser')
                games = soup.find_all("span", class_="title")
                game_prices = soup.find_all("div", class_="discount_final_price")
                games_full_prices = soup.find_all("div", class_="discount_original_price")
                games_percents = soup.find_all("div", class_="discount_pct")
                games_url = soup.find_all("a", class_="search_result_row")

                page_games = []

                # 🔹 Перебираем только доступные данные
                for game, price, full_price, percent, url in zip(games, game_prices, games_full_prices, games_percents,
                                                                 games_url):
                    img_tag = url.find("img")
                    img_url = img_tag["src"] if img_tag else "N/A"

                    page_games.append({
                        "title": game.text.strip(),
                        "price": price.text.strip() if price else "N/A",
                        "full_price": full_price.text.strip() if full_price else "N/A",
                        "percent": percent.text.strip() if percent else "N/A",
                        "url": url.get('href'),
                        "img": img_url
                    })

                # Если данных нет, отправляем пустой массив
                await self.send(text_data=json.dumps({"games": page_games, "page": page}))

            except httpx.RequestError as e:
                await self.send(text_data=json.dumps({"error": str(e)}))

    async def disconnect(self, close_code):
        self.keep_alive = False
        print(f"WebSocket отключен: {close_code}")
