import sys
from flask.cli import FlaskGroup
from api.src import create_app
from api.src.adapters.run_adapters import RequestAndBuild
import click

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('build_venues')
@click.argument('ll')
@click.argument('category')
def build_venues(ll, category):
    # "40.7,-74", "query": "tacos"
    runner = RequestAndBuild()
    runner.run(ll, category)
    print(ll, category)


if __name__ == "__main__":
    cli()
