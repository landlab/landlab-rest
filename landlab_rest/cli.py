# -*- coding: utf-8 -*-
import click

from .start import start


@click.command()
@click.version_option(prog_name="landlab-sketchbook")
@click.option("-p", "--port", default=80, help="port to run on")
@click.option("--host", default="0.0.0.0", help="host IP address")
@click.option("--silent", is_flag=True, help="only emit messages on error")
def main(host, port, silent):
    if not silent:
        click.secho("🚀 launching landlab sketchbook on {0}:{1}".format(host, port))
    start(host, port)
