from .aclient import AsyncClient

import asyncio

class ThreatMiner:

    async def _query_threatminer_rt(self, ip_address, rt):
        base_url = "https://api.threatminer.org/v2/host.php"
        params = {"q": ip_address, "rt": rt}
        async with AsyncClient() as client:
            response = await client.get(base_url, params=params)
            threat_data = response.json()
            return threat_data

    async def get_ip_tm_data(self, ip_address):
        # rt = 1  # Replace with the desired request type
        threat_data = await asyncio.gather(*[self._query_threatminer_rt(ip_address, rt) for rt in range(1,7)])
        self.threatminer_data = threat_data