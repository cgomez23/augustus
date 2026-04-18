from ..aclient import AsyncClient

class URLHaus:
    
    async def search_urlhaus_host(self, host):
        url = "https://urlhaus-api.abuse.ch/v1/host/"
        headers = {"Auth-Key": self._urlhaus_api_key}
        async with AsyncClient() as client:
            response = await client.post(url, data={"host": host}, headers=headers)
            self.urlhaus_data = response.json()
