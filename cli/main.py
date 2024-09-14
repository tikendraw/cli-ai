import click
import json
import os
from cli.config import config_file
from .app import app


@click.group()
def cli():
    """CLI AI: Natural Language Command Line Interface"""
    pass


def load_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)


@cli.command()
@click.argument("key_value", nargs=-1, type=click.UNPROCESSED)
def config(key_value):
    """View or set configuration values"""
    config = load_config()

    if not key_value:
        # If no arguments, print all configs
        if config:
            for k, v in config.items():
                click.echo(f"{k}: {v}")
        else:
            click.echo("No configuration values set.")
    elif len(key_value) == 2:
        # If two arguments, set the config
        key, value = key_value

        config[key] = value
        save_config(config)
        click.echo(f"Configuration '{key}' set to '{value}'")
    else:
        click.echo("Error: To set a config, provide a key and a value.")


@cli.command()
@click.argument("user_input", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--n-hist", type=int, default=2, help="Number of history items to consider"
)
@click.option("--model", help="Model name to use")
@click.option(
    "--error-report",
    "-er",
    type=bool,
    default=False,
    help="Fix the last error with current modifications",
)
def run(user_input, n_hist, model, error_report):
    """Run the main CLI AI application"""
    user_input_str = " ".join(user_input) if user_input else None

    config = load_config()
    ask_user = config.get("ask_user", "always")
    n_try = config.get("retry_generation", 3)

    if not model:
        model = config.get("default_model", "openai/gpt-3.5-turbo")

    app(
        user_input=user_input_str,
        n_hist=n_hist,
        model=model,
        error_report=error_report,
        ask_user=ask_user,
        n_try=n_try,
    )


if __name__ == "__main__":
    cli()
