from .aclient import AsyncClient

class Talos:

    async def get_talos_ip_data(self, ip_address):
        url = f"https://talosintelligence.com/cloud_intel/ip_reputation?ip={ip_address}"
        async with AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            self.talos_data = data
            
            # also avaiable in `data` object: volume_info, related_ips
