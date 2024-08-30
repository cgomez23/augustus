# TODO: modify requests to take in a url instead of hardcoding them in the functions


import asyncio

from ..osint import *

class IPv4(
    Pulsedive,
    ThreatMiner,
    SANS,
    Talos,
    OTX,
    ThreatFox,
    URLHaus
):
    def __init__(self, ipv4) -> None:

        self.ipv4 = ipv4
        self.function_map = {
            "threatminer_data": self.get_ip_tm_data,
            "sans_data": self.get_all_sans_ip_data,
            "talos_data": self.get_talos_ip_data,
            "pulsedive_data": self.get_pulsedive_ip_data,
            "otx_data": self.get_otx_ip_data,
            "threatfox_data": self.search_threatfox_ioc,
            "urlhaus_data": self.search_urlhaus_host
        }

    async def async_load_all_data(self):
        tasks = [func(self.ipv4) for func in self.function_map.values()]
        await asyncio.gather(*tasks)


class IPv4s:

    def __init__(self, ipv4s) -> None:
        self.ipv4s: list[str] = ipv4s
        self.ipv4_objs: list[IPv4] = []

    async def _async_load_all_ipv4s(self):
        self.ipv4_objs = [IPv4(ipv4) for ipv4 in self.ipv4s]
        tasks = [ipv4.async_load_all_data() for ipv4 in self.ipv4_objs]
        await asyncio.gather(*tasks)

    def load_all_ipv4s(self):
        asyncio.run(self._async_load_all_ipv4s())