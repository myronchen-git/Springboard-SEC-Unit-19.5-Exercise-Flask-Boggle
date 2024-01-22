from flask import Flask, jsonify, redirect, render_template, request, session
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


@app.route("/game/guess")
def route_guess():
    """Takes the word argument from the URL and checks if it is valid.  Returns a JSON."""

    if not request.args.get("word", ""):
        return "URL word argument can not be empty.", 400

    result = boggle_game.check_valid_word(session["board"], request.args["word"])
    return jsonify(result=result)
