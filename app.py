from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

# ==================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

boggle_game = Boggle()

# --------------------------------------------------
