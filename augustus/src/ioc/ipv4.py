import asyncio
import logging

from ..osint.nokey import Pulsedive, ThreatMiner, SANS, Talos, OTX, Shodan
from ..osint.key import ThreatFox, URLHaus
from ..config import get_api_key

logger = logging.getLogger("augustus")


class IPv4(
    Pulsedive,
    ThreatMiner,
    SANS,
    Talos,
    OTX,
    Shodan,
    URLHaus,
    ThreatFox,
):
    def __init__(self, ipv4) -> None:

        self.ipv4 = ipv4

        self.function_map = {
            # "threatminer_data": self.get_ip_tm_data,  # DEPRECATED: API returning 500
            "sans_data": self.get_all_sans_ip_data,
            "talos_data": self.get_talos_ip_data,
            "pulsedive_data": self.get_pulsedive_ip_data,
            "otx_data": self.get_otx_ip_data,
            "shodan_data": self.get_shodan_ip_data,
        }

        threatfox_key = get_api_key("threatfox")
        if threatfox_key:
            self._threatfox_api_key = threatfox_key
            self.function_map["threatfox_data"] = self.search_threatfox_ioc
            logger.info("ThreatFox API key found, enabling ThreatFox enrichment")

        urlhaus_key = get_api_key("urlhaus")
        if urlhaus_key:
            self._urlhaus_api_key = urlhaus_key
            self.function_map["urlhaus_data"] = self.search_urlhaus_host
            logger.info("URLHaus API key found, enabling URLHaus enrichment")


class IPv4s:

    def __init__(self, ipv4s) -> None:
        self.ipv4s: list[str] = ipv4s
        self.ipv4_objs: list[IPv4] = []

    async def _async_load_all_ipv4s(self):
        self.ipv4_objs = [IPv4(ipv4) for ipv4 in self.ipv4s]
        tasks = [
            func(ipv4.ipv4) 
            for ipv4 in self.ipv4_objs 
            for func in ipv4.function_map.values()
        ]
        await asyncio.gather(*tasks)

    def load_all_ipv4s(self):
        asyncio.run(self._async_load_all_ipv4s())
