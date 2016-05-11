from pilgrim3.app import app
import pkg_resources
import os
import click


@click.command()
@click.option('--port', default=9151, help='port')
@click.option('--host', default='localhost', help='host')
@click.option('--proto-bundle', help='path to proto bundle')
def main(host, port, proto_bundle):
    app.config['proto-google'] = pkg_resources.resource_filename("pilgrim3", "data/proto_bundle")
    app.config['proto-bundle'] = os.path.abspath(proto_bundle)
    app.run(host=host, port=port, threaded=True)
