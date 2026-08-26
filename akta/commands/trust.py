import click
import httpx

BASE_URL = "http://localhost:8050/api/v1/trust"

@click.group()
def trust():
    """TrustChain-AI commands for agent trust management"""
    pass

@trust.command()
@click.argument("did")
def score(did):
    """Get the current trust score for an agent"""
    try:
        response = httpx.get(f"{BASE_URL}/state/{did}")
        response.raise_for_status()
        data = response.json()
        click.echo(f"Agent: {data['agent_did']}")
        click.echo(f"Trust Score: {data['temporal_trust_score']:.4f}")
    except httpx.HTTPStatusError as e:
        click.echo(f"Error: {e.response.text}")
    except Exception as e:
        click.echo(f"Error connecting to server: {e}")

@trust.command()
@click.argument("did")
def state(did):
    """Get the current trust state for an agent"""
    try:
        response = httpx.get(f"{BASE_URL}/state/{did}")
        response.raise_for_status()
        data = response.json()
        click.echo(f"Agent: {data['agent_did']}")
        click.echo(f"Trust State: {data['trust_state']}")
    except httpx.HTTPStatusError as e:
        click.echo(f"Error: {e.response.text}")
    except Exception as e:
        click.echo(f"Error connecting to server: {e}")

@trust.command()
@click.argument("did")
def audit(did):
    """Get the trust transition audit trail for an agent"""
    try:
        response = httpx.get(f"{BASE_URL}/audit/{did}")
        response.raise_for_status()
        data = response.json()
        if not data:
            click.echo(f"No audit trail found for {did}")
            return
        
        click.echo(f"Audit Trail for {did}:")
        for record in data:
            click.echo(f"[{record['timestamp']}] {record['previous_state']} -> {record['new_state']} | Reason: {record['reason']}")
    except httpx.HTTPStatusError as e:
        click.echo(f"Error: {e.response.text}")
    except Exception as e:
        click.echo(f"Error connecting to server: {e}")

@trust.command()
@click.argument("did")
@click.option("--reason", default="Administrative action", help="Reason for revocation")
def revoke(did, reason):
    """Administratively revoke an agent's trust state"""
    try:
        response = httpx.post(f"{BASE_URL}/revoke/{did}", json={"reason": reason})
        response.raise_for_status()
        data = response.json()
        click.echo(f"Successfully revoked {did}")
        click.echo(f"New State: {data['trust_state']}")
    except httpx.HTTPStatusError as e:
        click.echo(f"Error: {e.response.text}")
    except Exception as e:
        click.echo(f"Error connecting to server: {e}")

@trust.command()
def agents():
    """List all agents and their trust states"""
    try:
        response = httpx.get(f"{BASE_URL}/agents")
        response.raise_for_status()
        data = response.json()
        if not data:
            click.echo("No agents found.")
            return
        
        for s in data:
            click.echo(f"{s['agent_did']} | Score: {s['trust_score']:.4f} | State: {s['trust_state']}")
    except httpx.HTTPStatusError as e:
        click.echo(f"Error: {e.response.text}")
    except Exception as e:
        click.echo(f"Error connecting to server: {e}")
