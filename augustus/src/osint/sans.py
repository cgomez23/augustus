from .aclient import AsyncClient

from asyncio import gather
from bs4 import BeautifulSoup


class SANS:
    
    # https://isc.sans.edu/ipdetails.html?ip=
    
    async def get_ip_traffic(self, ip_address):
        url = f"https://isc.sans.edu/ipdetails.html?ip={ip_address}"
        async with AsyncClient() as client:
            response = await client.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {"aria-label":"ip address summary"})

            headers = [th.text for th in table.find('tr').find_all('th')] # type: ignore
            data = []
            for row in table.find_all('tr')[1:]: # type: ignore
                row_data = {headers[i]:td.text.strip() for i, td in enumerate(row.find_all('td'))}
                data.append(row_data)
            return data
    
    async def get_weblog_dates(self, ip_address):
        url = f"https://isc.sans.edu/ipinfo/{ip_address}"
        async with AsyncClient() as client:
            response = await client.get(url)

            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {"aria-label":"web honeypot logs"})  # Example class selector
            if not table:
                return []
            # return list of date strings
            return [d.find_all('td')[0].text for d in table.find('tbody').find_all('tr')] # type: ignore
    
    async def get_sans_ip_data(self, ip_address):
        url = f"https://isc.sans.edu/api/ip/{ip_address}?json"
        async with AsyncClient() as client:
            response = await client.get(url)
            return response.json()
            
    async def get_sans_weblog_data(self, ip_address, date):
        url = f"https://isc.sans.edu/api/webhoneypotreportsbysource/{ip_address}/{date}?json"
        async with AsyncClient() as client:
            response = await client.get(url)
            return {date:response.json()}
            
            
    async def get_all_sans_ip_data(self, ip_address):
        sans_ip_data = await self.get_sans_ip_data(ip_address)
        traffic_data = await self.get_ip_traffic(ip_address)
        weblog_dates = await self.get_weblog_dates(ip_address)
        if weblog_dates:
            sans_weblog_data = await gather(*[self.get_sans_weblog_data(ip_address, date) for date in weblog_dates])
        else:
            sans_weblog_data = []
        self.sans_data = {'ip_data': sans_ip_data, 'weblog_data': sans_weblog_data, 'honeypot_traffic_data': traffic_data}