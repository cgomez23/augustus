import httpx, httpcore
import logging
# coloredlogs.install()
# from colorlog import ColoredFormatter
from rich.logging import RichHandler
from urllib.parse import urlparse

# FORMAT = "%(log_color)s%(asctime)s - %(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s"
FORMAT = "%(levelname)s %(message)s"

# logging.root.setLevel(LOG_LEVEL)
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(tracebacks_suppress=[httpx, httpcore])]
)
# formatter = ColoredFormatter(LOGFORMAT)
logger = logging.getLogger('rich')
logging.getLogger("httpx").setLevel(logging.CRITICAL)



class AsyncClient(httpx.AsyncClient):

    def __init__(self) -> None:
        super().__init__()

        self.timeout = httpx.Timeout(30.0)

    async def get(self, url, **kwargs):
        """Override the get method to handle errors"""
        protocol = urlparse(url).scheme
        domain = urlparse(url).netloc
        endpoint = urlparse(url).path + '?' + urlparse(url).query

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        try:
            logger.info(f"{protocol.upper()} GET: {url} {kwargs}")
            resp = await super().get(url, **kwargs)
            if 200 <= resp.status_code <= 299:
                logger.info(f"[bold grey37 blink]{domain}[/]: Success {resp.status_code}: {endpoint} {kwargs}", extra={"markup": True})
                return resp
            elif resp.status_code == 404:
                logger.warning(f"[bold grey37 blink]{domain}[/]: Warning {resp.status_code} Not Found: {url}")
                return httpx.Response(status_code=404, json={})
            else:
                logger.error(f"[bold grey37 blink]{domain}[/]: Error {resp.status_code}: Unable to query {url}")
                return httpx.Response(status_code=resp.status_code, json={})
        except httpx.RequestError as e:
            logger.critical(f"Critical: {resp.status_code} - {e}")
            return httpx.Response(status_code=500, json={})
        
    async def post(self, url, **kwargs):
        """Override the get method to handle errors"""
        protocol = urlparse(url).scheme
        domain = urlparse(url).netloc
        endpoint = urlparse(url).path + '?' + urlparse(url).query

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        try:
            logger.info(f"{protocol.upper()} POST: {url} {kwargs}")
            resp = await super().post(url, **kwargs)
            if 200 <= resp.status_code <= 299:
                logger.info(f"[bold grey37 blink]{domain}[/]: Success {resp.status_code}: {endpoint} {kwargs}", extra={"markup": True})
                return resp
            elif resp.status_code == 404:
                logger.warning(f"[bold grey37 blink]{domain}[/]: Warning {resp.status_code} Not Found: {url}")
                return httpx.Response(status_code=404, json={})
            else:
                logger.error(f"[bold grey37 blink]{domain}[/]: Error {resp.status_code}: Unable to query {url}")
                return httpx.Response(status_code=resp.status_code, json={})
        except httpx.RequestError as e:
            logger.critical(f"Critical: {resp.status_code} - {e}")
            return httpx.Response(status_code=500, json={})