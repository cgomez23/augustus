from ..aclient import AsyncClient


class Shodan:

    async def get_shodan_ip_data(self, ip_address: str):
        url = f"https://api.shodan.io/shodan/host/{ip_address}"
        async with AsyncClient() as client:
            response = await client.get(url)
            self.shodan_data = response.json()
