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

    return render_template(
        "game.html",
        board=board,
        games_played=session.get("games_played", 0),
        high_score=session.get("high_score", 0),
    )


@app.route("/game/guess")
def route_guess():
    """Takes the word argument from the URL and checks if it is valid.  Returns a JSON with the result."""

    if not request.args.get("word", ""):
        return "URL word argument can not be empty.", 400

    result = boggle_game.check_valid_word(session["board"], request.args["word"])
    return jsonify(result=result)


@app.route("/game/highscore", methods=["post"])
def route_highscore():
    """Increments the number of games played and updates the high score.  Returns the high score."""

    if request.json is not None:
        points = request.json.get("points")

        if points is not None and points >= 0:
            session["games_played"] = session.get("games_played", 0) + 1

            high_score = session.get("high_score", 0)
            if points > high_score:
                high_score = points

            session["high_score"] = high_score

            return jsonify({"highScore": high_score})

    return "Need to pass positive integer points in JSON.", 400
