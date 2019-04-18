# -*- coding: utf-8 -*-
import click

from .start import start


@click.command()
@click.version_option(prog_name="landlab-sketchbook")
@click.option("-p", "--port", default=80, help="port to run on")
@click.option("--host", default="0.0.0.0", help="host IP address")
def main(host, port):
    click.secho("🚀 launching landlab sketchbook on {0}:{1}".format(host, port))
    start(host, port)
