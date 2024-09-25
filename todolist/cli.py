from typing import Optional
from pathlib import Path
from todolist import ERRORS,__app_name__,__version__,config,database

import typer

from todolist import __app_name__ , __version__

app = typer.Typer()
@app.command()
def init(
    db_path:str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db--path",
        "--db",
        prompt="to-do database location?",
    ),
) -> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}",fg=typer.colors.GREEN)

def _version_callback(value:bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v {__version__}")
        raise typer.Exit()
    
@app.callback()

def main(
    version: Optional[bool]= typer.Option(
        None,
        "--version",
        "-v",
        help="show the application's version and exit",
        callback=_version_callback,
        is_eager=True,
    )

) -> None:
    return