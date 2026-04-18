import os
import sys
import logging
import click
import json

from rich.logging import RichHandler

import augustus

from .src.ioc.ipv4 import IPv4s

logging.basicConfig(
    level=getattr(logging, os.getenv("LOGLEVEL", "INFO").upper()),
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)]
)

logger = logging.getLogger("augustus")

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

@click.group()
@click.version_option()
def cli():
    "A comprehensive IOC enrichment tool from OSINT sources"
    
@cli.command()
@click.option("-v", "--verbose", count=True)
def version(verbose):
    """Displays the version"""
    click.echo("Version: %s" % augustus.__version__)
    if verbose > 0:
        click.echo("Author: %s" % augustus.__author__)

@cli.command()
@click.argument("ips")
def equery(ips: str):
    "Command to enrich IOCs from all intel services."
    ips = ips.split(",") # type: ignore

    ipv4s = IPv4s(ips)
    ipv4s.load_all_ipv4s()
    for ipv4 in ipv4s.ipv4_objs:
        d = {
            name.removesuffix("_data"): getattr(ipv4, name)
            for name in ipv4.function_map
        }
        
        with open("output.json", "w") as f:
            f.write(json.dumps(d, indent=4))


if __name__ == "__main__":
    cli(prog_name="augustus")
