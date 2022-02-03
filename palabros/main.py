import typer

from palabros import business, console, database
from palabros.errors import DatabaseError, GameError

database.init()
app = typer.Typer()


@app.command("play")
def _play_game(word: str) -> None:

    """
    Try to guess the seed word using WORD.
    \f

    Args:
        word: The word which he player is playing with.

    Raises:
        Exit: if an error occurred while executing the command.
    """

    if len(word) != business.WORD_LENGTH:
        console.print_error(f"La palabra tiene que tener [bold]{business.WORD_LENGTH}[/] letras")
        raise typer.Exit()

    if not business.word_exists(word):
        console.print_error(f"La palabra [bold]{word}[/] no existe en el diccionario")
        raise typer.Exit()

    try:
        game = business.get_current_game()

        if not game.any_match() and game.any_attempt_left():
            attempt = business.play_game(game, word)
            game.attempts.append(attempt)

    except (DatabaseError, GameError) as err:
        console.print_error(err.message)
    except Exception as err:
        console.print_error(f"Error no controlado: {str(err)}")
    else:
        console.print_result(game)


@app.command("results")
def _view_results(date: str) -> None:

    """
    Check the results of a given DATE.
    \f

    Args:
        date: The date, given in YYYYMMDD format.

    Raises:
        Exit: if an error occurred while executing the command.
    """

    console.print_error("Esta funcionalidad aún no está implementada")
    raise typer.Exit()


if __name__ == "__main__":
    app()
