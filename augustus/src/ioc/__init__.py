from .ipv4 import IPv4s

import re

def _identify_ioc_type(ioc: str) -> str:
    # Patterns for each type
    patterns = {
        "ipv4": r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
        "ipv6": r'^([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|'
                r'([0-9a-fA-F]{1,4}:){1,7}:|'
                r'([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
                r'([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|'
                r'([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|'
                r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|'
                r'([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|'
                r'[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|'
                r':((:[0-9a-fA-F]{1,4}){1,7}|:)|'
                r'fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|'
                r'::(ffff(:0{1,4}){0,1}:){0,1}'
                r'((25[0-5]|(2[0-4]|1{0,1}[0-9]{0,1}[0-9]?)\.){3}'
                r'(25[0-5]|(2[0-4]|1{0,1}[0-9]{0,1}[0-9]?))|'
                r'([0-9a-fA-F]{1,4}:){1,4}:([0-9a-fA-F]{1,4}|:))$',
        "cve": r'^CVE-\d{4}-\d+$',
        "url": r'^(https?://[^\s/$.?#].[^\s]*)$',
        "md5": r'^[a-fA-F0-9]{32}$',
        "sha1": r'^[a-fA-F0-9]{40}$',
        "sha256": r'^[a-fA-F0-9]{64}$',
        "fqdn": r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$',
        "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    }
    
    for type_name, pattern in patterns.items():
        if re.match(pattern, ioc):
            return type_name
    
    return "Unknown"

def load_iocs(iocs: str) -> list:
    indicators = iocs.split(",")
    return [IOC(indicator) for indicator in indicators]

class IOC:
    
    # todo: change ipv4 to include `ioc` field in the constructor
    def __init__(self, ioc: str):
        self.ioc = ioc
        self.ioc_type = _identify_ioc_type(ioc)
        

# class IOCs:
#     def __init__(self, iocs: str):
        
#         self.ipv4s = []
#         self.ipv6s = []
#         self.cves = []
#         self.urls = []
#         self.md5s = []
#         self.sha1s = []
#         self.sha256s = []
#         self.fqdns = []
#         self.emails = []
        
#         indicators = iocs.split(",")
#         self._parse_iocs(indicators)
        
        
#     def _parse_iocs(self, iocs: list[str]):
#         for ioc in iocs:
#             ioc_type = identify_ioc_type(ioc)
#             if ioc_type == "ipv4":
#                 self.ipv4s.append(ioc)
#             elif ioc_type == "ipv6":
#                 self.ipv6s.append(ioc)
#             elif ioc_type == "cve":
#                 self.cves.append(ioc)
#             elif ioc_type == "url":
#                 self.urls.append(ioc)
#             elif ioc_type == "md5":
#                 self.md5s.append(ioc)
#             elif ioc_type == "sha1":
#                 self.sha1s.append(ioc)
#             elif ioc_type == "sha256":
#                 self.sha256s.append(ioc)
#             elif ioc_type == "fqdn":
#                 self.fqdns.append(ioc)
#             elif ioc_type == "email":
#                 self.emails.append(ioc)