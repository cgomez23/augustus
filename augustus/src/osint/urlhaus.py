from .aclient import AsyncClient

class URLHaus:
    
    async def search_urlhaus_host(self, host):
        url = "https://urlhaus-api.abuse.ch/v1/host/"
        async with AsyncClient() as client:
            response = await client.post(url, data={"host": host})
            self.urlhaus_data = response.json()