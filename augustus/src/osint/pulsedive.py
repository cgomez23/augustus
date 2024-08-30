from .aclient import AsyncClient

class Pulsedive:

    async def get_pulsedive_ip_data(self, ip_address: str):
        url = f"https://pulsedive.com/api/info.php?indicator={ip_address}&historical=true&schema=0&pretty=0"
        async with AsyncClient() as client:
            response = await client.get(url)
            self.pulsedive_data = response.json()
