from .aclient import AsyncClient

class ThreatFox:
    
    async def search_threatfox_ioc(self, ioc):
        url = "https://threatfox-api.abuse.ch/api/v1/"
        async with AsyncClient() as client:
            response = await client.post(url, json={"query": "search_ioc", "search_term": ioc})
            self.threatfox_data = response.json()