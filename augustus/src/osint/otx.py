import asyncio

from .aclient import AsyncClient

OTX_ENDPOINTS = ["", "geo", "malware", "url_list", "passive_dns", "http_scans"]
OTX_ANALYSIS_URL = "https://otx.alienvault.com/otxapi/indicators/ip/analysis/"

class OTX:
    async def _get_ip_endpoint(self, ip_address: str, endpoint: str) -> dict:
        url = f"https://otx.alienvault.com/api/v1/indicator/IPv4/{ip_address}/{endpoint}"
        async with AsyncClient() as client:
            response = await client.get(url)
            return {endpoint:response.json()}

    async def _get_ip_analysis_info(self, ip_address: str) -> dict:
        url = OTX_ANALYSIS_URL + ip_address
        async with AsyncClient() as client:
            response = await client.get(url)
            return {"analysis":response.json()}

    async def get_otx_ip_data(self, ip_address: str):
        tasks = [self._get_ip_endpoint(ip_address, endpoint) for endpoint in OTX_ENDPOINTS] + \
            [self._get_ip_analysis_info(ip_address)]
        
        data = await asyncio.gather(*tasks)
        self.otx_data = {k:v for d in data for k, v in d.items()}
        