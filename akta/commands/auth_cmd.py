import getpass
import click
from akta.vdr.database import SessionLocal, create_tables
from akta.auth import crud


@click.group()
def auth():
    """Authentication and User Security Management Commands"""
    pass


@auth.command(name="create-admin")
@click.option("--username", prompt="Admin Username", help="Username for the new admin account")
@click.option("--email", prompt="Admin Email", help="Email address for the new admin account")
def create_admin(username, email):
    """Interactively creates a new administrative user account."""
    create_tables()
    password = getpass.getpass("Enter Admin Password (min 8 chars): ")
    confirm_password = getpass.getpass("Confirm Admin Password: ")

    if password != confirm_password:
        click.echo("Error: Passwords do not match.", err=True)
        return

    if len(password) < 8:
        click.echo("Error: Password must be at least 8 characters long.", err=True)
        return

    db = SessionLocal()
    try:
        user = crud.create_user(
            db=db,
            username=username.strip(),
            email=email.strip(),
            password=password,
            role="ADMIN",
            is_active=True,
            created_by_admin=True
        )
        click.echo(f"SUCCESS: Admin account '{user.username}' (ID: {user.id}) created successfully.")
    except Exception as e:
        click.echo(f"Error creating admin account: {e}", err=True)
    finally:
        db.close()


@auth.command(name="user-list")
def user_list():
    """Lists all registered platform application users."""
    create_tables()
    db = SessionLocal()
    try:
        from akta.vdr import models
        users = db.query(models.UserModel).order_by(models.UserModel.created_at.desc()).all()
        if not users:
            click.echo("No users registered.")
            return

        click.echo(f"\nRegistered Platform Users ({len(users)} total):")
        click.echo("-" * 80)
        click.echo(f"{'ID':<36} | {'Username':<16} | {'Role':<10} | {'Active':<6} | {'Email'}")
        click.echo("-" * 80)
        for u in users:
            click.echo(f"{u.id:<36} | {u.username:<16} | {u.role:<10} | {str(u.is_active):<6} | {u.email}")
        click.echo("-" * 80)
    finally:
        db.close()


@auth.command(name="disable-user")
@click.argument("user_id")
def disable_user(user_id):
    """Disables a user account and revokes active sessions."""
    create_tables()
    db = SessionLocal()
    try:
        user = crud.update_user_status(db, user_id=user_id, is_active=False)
        click.echo(f"SUCCESS: Account '{user.username}' (ID: {user.id}) has been disabled.")
    except Exception as e:
        click.echo(f"Error disabling user: {e}", err=True)
    finally:
        db.close()


@auth.command(name="enable-user")
@click.argument("user_id")
def enable_user(user_id):
    """Enables a disabled user account."""
    create_tables()
    db = SessionLocal()
    try:
        user = crud.update_user_status(db, user_id=user_id, is_active=True)
        click.echo(f"SUCCESS: Account '{user.username}' (ID: {user.id}) has been enabled.")
    except Exception as e:
        click.echo(f"Error enabling user: {e}", err=True)
    finally:
        db.close()


@auth.command(name="revoke-sessions")
@click.argument("user_id")
def revoke_sessions(user_id):
    """Revokes all active refresh token sessions for a specific user ID."""
    create_tables()
    db = SessionLocal()
    try:
        crud.revoke_all_user_sessions(db, user_id=user_id, reason="Sessions revoked via CLI command")
        click.echo(f"SUCCESS: All refresh token sessions for user ID '{user_id}' have been revoked.")
    except Exception as e:
        click.echo(f"Error revoking sessions: {e}", err=True)
    finally:
        db.close()
