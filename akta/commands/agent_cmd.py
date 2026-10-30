import json
from typing import Optional
import click
import httpx
from akta.config import settings

BASE_URL = f"http://{settings.host}:{settings.port}/api/v1"

@click.group("agent")
def agent_cmd():
    """Register, discover, check health, and manage AI Agents"""
    pass

@agent_cmd.command("list")
@click.option("--capability", help="Filter by capability")
@click.option("--status", help="Filter by operational status (AVAILABLE, BUSY, OFFLINE)")
def list_agents(capability: Optional[str], status: Optional[str]):
    """Lists registered agents in the TrustChain network."""
    params = {}
    if capability:
        params["capability"] = capability
    if status:
        params["status"] = status

    try:
        resp = httpx.get(f"{BASE_URL}/registry/agents", params=params)
        resp.raise_for_status()
        agents = resp.json()
        click.echo(click.style(f"\nTracked Agents ({len(agents)} total):", fg="cyan", bold=True))
        for a in agents:
            status_color = "green" if a["operational_status"] == "AVAILABLE" else "yellow"
            trust_color = "green" if a["trust_state"] == "TRUSTED" else "red"
            ts = a['trust_score']
            t_state = a['trust_state']
            trust_str = click.style(f"{ts:.4f} [{t_state}]", fg=trust_color)
            click.echo(
                f"  - {click.style(a['agent_name'], bold=True)} ({a['did'][:24]}...)\n"
                f"    Provider: {a['model_provider']} | Model: {a['model_name']} | Caps: {a['capabilities']}\n"
                f"    Status: {click.style(a['operational_status'], fg=status_color)} | "
                f"Health: {a['health_status']} | "
                f"Trust: {trust_str} | "
                f"Reputation: {a['reputation_score']}/5.0\n"
            )
    except Exception as e:
        click.echo(click.style(f"Error fetching agent list: {e}", fg="red"))

@agent_cmd.command("register")
@click.option("--name", "-n", required=True, help="Agent Name")
@click.option("--type", "-t", default="general", help="Agent Type (research, analysis, coding, etc.)")
@click.option("--capabilities", "-c", default="general", help="Capabilities (comma-separated)")
@click.option("--provider", "-p", default="OpenAI", help="Model Provider")
@click.option("--model", "-m", default="gpt-4o", help="Model Name")
@click.option("--endpoint", "-e", help="Optional HTTP Endpoint URL")
def register_agent(name: str, type: str, capabilities: str, provider: str, model: str, endpoint: Optional[str]):
    """Registers a new AI agent with persistent Ed25519 identity."""
    payload = {
        "agent_name": name,
        "agent_type": type,
        "capabilities": capabilities,
        "model_provider": provider,
        "model_name": model,
        "endpoint": endpoint
    }
    try:
        resp = httpx.post(f"{BASE_URL}/registry/agents", json=payload)
        resp.raise_for_status()
        data = resp.json()
        click.echo(click.style(f"Agent '{name}' registered successfully!", fg="green", bold=True))
        click.echo(f"  Agent ID:   {data['agent_id']}")
        click.echo(f"  DID:        {data['did']}")
        click.echo(f"  Status:     {data['operational_status']}")
        click.echo(f"  TrustState: {data['trust_state']} ({data['trust_score']})")
    except Exception as e:
        click.echo(click.style(f"Error registering agent: {e}", fg="red"))

@agent_cmd.command("discover")
@click.option("--capability", "-c", required=True, help="Required capability")
def discover_agents(capability: str):
    """Discovers available (free, healthy, trusted) candidate agents matching capability."""
    try:
        resp = httpx.get(f"{BASE_URL}/registry/discover", params={"capability": capability})
        resp.raise_for_status()
        candidates = resp.json()
        click.echo(click.style(f"\nAvailable Candidates for '{capability}' ({len(candidates)} total):", fg="cyan", bold=True))
        for c in candidates:
            click.echo(f"  - {c['agent_name']} ({c['did']}) | Trust: {c['trust_score']:.3f} | Rep: {c['reputation_score']}/5.0")
    except Exception as e:
        click.echo(click.style(f"Error discovering agents: {e}", fg="red"))

@agent_cmd.command("health")
@click.argument("did_or_id")
def check_health(did_or_id: str):
    """Triggers an active endpoint health check for an agent."""
    try:
        resp = httpx.post(f"{BASE_URL}/registry/agents/{did_or_id}/health")
        resp.raise_for_status()
        data = resp.json()
        color = "green" if data["health_status"] == "HEALTHY" else "red"
        click.echo(click.style(f"\nHealth Check Result for {data['agent_name']}:", fg="cyan", bold=True))
        click.echo(f"  Status:         {click.style(data['health_status'], fg=color, bold=True)}")
        click.echo(f"  Response Time:  {data['response_time_ms']} ms")
        if data["last_error"]:
            click.echo(click.style(f"  Error:          {data['last_error']}", fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"Error checking agent health: {e}", fg="red"))
