import click

from akta.commands.claim import claim
from akta.commands.keys import keys
from akta.commands.registry import registry
from akta.commands.token import token
from akta.commands.vdr import vdr
from akta.commands.trust import trust
from akta.commands.agent_cmd import agent_cmd
from akta.commands.auth_cmd import auth


@click.group()
def cli():
    """Acta - Authenticated Knowledge & Trust Architecture for AI Agents"""
    pass


cli.add_command(keys)
cli.add_command(claim)
cli.add_command(token)
cli.add_command(registry)
cli.add_command(vdr)
cli.add_command(trust)
cli.add_command(agent_cmd, name="agent")
cli.add_command(auth)


if __name__ == "__main__":
    cli()