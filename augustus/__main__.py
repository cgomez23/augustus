import os
import sys
import logging
import click
import json

import augustus

from .src.iocs.ipv4 import IPv4s

if sys.stdout.isatty():
# You're running in a real terminal
    LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
else:
    LOG_FORMAT="%(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=getattr(logging, os.getenv("LOGLEVEL", "INFO").upper()),
    format=LOG_FORMAT,
    datefmt="%Y-%m-%dT%H:%M:%S"
)

logger = logging.getLogger("augustus")

# set levels for other modules
logging.getLogger("urllib3").setLevel(logging.WARNING)

@click.group()
@click.version_option()
# @click.option(
#     "-p",
#     "--pulsedive",
#     help="Include PulseDive data (Rate-limited to 9 queries a day)",
# )
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
def ip(ips: str):
    "Command to enrich IP addresses"
    ips = ips.split(",") # type: ignore

    ipv4s = IPv4s(ips)
    ipv4s.load_all_ipv4s()
    for ipv4 in ipv4s.ipv4_objs:
        d = {
            "threatminer": ipv4.threatminer_data,
            "sans": ipv4.sans_data,
            "talos": ipv4.talos_data['reputation'],
            "pulsedive": ipv4.pulsedive_data,
            "otx": ipv4.otx_data,
            "threatfox": ipv4.threatfox_data,
            "urlhaus": ipv4.urlhaus_data
        }
        
        # del d["Pulsedive Data"].properties
        
        d['otx']['']['pulse_info']['pulses'] = [
            {
                'name': pulse['name'], 'description': pulse['description']
            } for pulse in d['otx']['']['pulse_info']['pulses']]
        
        with open("output.json", "w") as f:
            f.write(json.dumps(d, indent=4))


if __name__ == "__main__":
    cli(prog_name="augustus")
