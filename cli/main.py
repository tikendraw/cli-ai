import click
import json
import os
from config import config_folder

@click.group()
def cli():
    """CLI AI: Natural Language Command Line Interface"""
    pass

@cli.command()
@click.argument('key')
@click.argument('value')
def set_config(key, value):
    """Set a configuration value"""
    config_file = os.path.join(config_folder, "config.json")
    
    # Load existing config or create new
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    # Update config
    config[key] = value
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    click.echo(f"Configuration '{key}' set to '{value}'")

@cli.command()
@click.argument('key', required=False)
def get_config(key):
    """Get a configuration value or list all"""
    config_file = os.path.join(config_folder, "config.json")
    
    if not os.path.exists(config_file):
        click.echo("No configuration file found.")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    if key:
        if key in config:
            click.echo(f"{key}: {config[key]}")
        else:
            click.echo(f"Configuration '{key}' not found.")
    else:
        for k, v in config.items():
            click.echo(f"{k}: {v}")

@cli.command()
def run():
    """Run the main CLI AI application"""
    from cli.app import app
    app()

if __name__ == '__main__':
    cli()
