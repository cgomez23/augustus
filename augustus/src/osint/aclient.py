import time

import httpx
import logging
from urllib.parse import urlparse

logger = logging.getLogger("augustus")

DEFAULT_TIMEOUT = 10.0


class AsyncClient(httpx.AsyncClient):

    def __init__(self, timeout: float = DEFAULT_TIMEOUT, user_agent: str | None = None) -> None:
        headers = {"User-Agent": user_agent} if user_agent else {}
        super().__init__(
            timeout=httpx.Timeout(timeout),
            headers=headers,
        )
        self.transport = httpx.AsyncHTTPTransport(retries=3)
        self._request_timeout = timeout

    async def get(self, url, **kwargs):
        """Override the get method with retry-until-timeout behavior"""
        domain = urlparse(url).netloc
        deadline = time.monotonic() + self._request_timeout

        while True:
            try:
                resp = await super().get(url, **kwargs)
                if 200 <= resp.status_code <= 299:
                    logger.info(f"{domain}: GET {resp.status_code} {url}")
                    return resp
                elif resp.status_code == 404:
                    logger.warning(f"{domain}: GET {resp.status_code} {url}")
                    return httpx.Response(status_code=404, json={})
                else:
                    logger.error(f"{domain}: GET {resp.status_code} {url}")
                    return httpx.Response(status_code=resp.status_code, json={})
            except httpx.TimeoutException:
                if time.monotonic() >= deadline:
                    logger.error(f"{domain}: Timeout after {self._request_timeout}s {url}")
                    return httpx.Response(status_code=500, json={})
                logger.warning(f"{domain}: Timeout, retrying {url}")
            except httpx.RequestError as e:
                logger.error(f"{domain}: {type(e).__name__} {url}")
                return httpx.Response(status_code=500, json={})

    async def post(self, url, **kwargs):
        """Override the post method with retry-until-timeout behavior"""
        domain = urlparse(url).netloc
        deadline = time.monotonic() + self._request_timeout

        while True:
            try:
                resp = await super().post(url, **kwargs)
                if 200 <= resp.status_code <= 299:
                    logger.info(f"{domain}: POST {resp.status_code} {url}")
                    return resp
                elif resp.status_code == 404:
                    logger.warning(f"{domain}: POST {resp.status_code} {url}")
                    return httpx.Response(status_code=404, json={})
                else:
                    logger.error(f"{domain}: POST {resp.status_code} {url}")
                    return httpx.Response(status_code=resp.status_code, json={})
            except httpx.TimeoutException:
                if time.monotonic() >= deadline:
                    logger.error(f"{domain}: Timeout after {self._request_timeout}s {url}")
                    return httpx.Response(status_code=500, json={})
                logger.warning(f"{domain}: Timeout, retrying {url}")
            except httpx.RequestError as e:
                logger.error(f"{domain}: {type(e).__name__} {url}")
                return httpx.Response(status_code=500, json={})
