from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

# ==================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

boggle_game = Boggle()

# --------------------------------------------------


@app.route("/")
def route_root():
    """Currently redirects to the game.  In the future, this will display a page to input board size."""

    return redirect("/game")


@app.route("/game")
def route_game():
    """Displays the game board and a form to submit a word."""

    board = boggle_game.make_board()

    session["board"] = board

    return render_template("game.html", board=board)
