import string
from unittest import TestCase

from flask import session

from app import app
from boggle import Boggle

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


class FlaskTests(TestCase):
    """Tests for the game."""

    SESSION_KEY_GAMES_PLAYED = "games_played"
    SESSION_KEY_HIGH_SCORE = "high_score"
    JSON_KEY_HIGHSCORE = "highScore"
    JSON_KEY_RESULT = "result"

    def setUp(self):
        self.client = app.test_client()

    def test_root_redirect(self):
        """Tests for redirection."""

        with self.client as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/game")

    def test_board_creation(self):
        """Tests that the board is created in the HTML."""

        with self.client as client:
            resp = client.get("/game")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("<table", html)
            self.assertIn("<tr", html)
            self.assertIn("<td", html)

    def test_board_saving_in_session(self):
        """Tests that the board is saved to a Flask session cookie."""

        with self.client as client:
            resp = client.get("/game")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("board", session)
            self.assertEqual(len(session["board"]), 5)
            self.assertEqual(len(session["board"][0]), 5)
            self.assertIn(session["board"][0][0], string.ascii_uppercase)

    def test_form_creation(self):
        """Tests that the form is created on the HTML."""

        with self.client as client:
            resp = client.get("/game")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("</form>", html)
            self.assertIn('name="guessed-word"', html)

    def test_header_creation(self):
        """Tests that all the things in the header are created."""

        with self.client as client:
            resp = client.get("/game")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('id="games-played"', html)
            self.assertIn('id="high-score"', html)
            self.assertIn('id="points"', html)

    def test_valid_word_submission(self):
        """Tests for a word that exists in the words list and on the board."""

        with self.client as client:
            self.save_board_to_session(client)

            resp = client.get("/game/guess?word=cat")
            self.assertEqual(resp.json[self.JSON_KEY_RESULT], "ok")

    def test_invalid_word_submission(self):
        """Tests for a word that exists in the words list but not on the board."""

        with self.client as client:
            self.save_board_to_session(client)

            resp = client.get("/game/guess?word=zoozoo")
            self.assertEqual(resp.json[self.JSON_KEY_RESULT], "not-on-board")

    def test_nonword_submission(self):
        """Tests for nonwords."""

        with self.client as client:
            self.save_board_to_session(client)

            resp = client.get("/game/guess?word=zzzz")
            self.assertEqual(resp.json[self.JSON_KEY_RESULT], "not-a-word")

            resp = client.get("/game/guess?word=555")
            self.assertEqual(resp.json[self.JSON_KEY_RESULT], "not-a-word")

    def test_incorrect_syntax_for_word_submission(self):
        """Tests for incorrect URL syntax when guessing a word."""

        with self.client as client:
            resp = client.get("/game/guess?word=")
            self.assertEqual(resp.status_code, 400)

            resp = client.get("/game/guess")
            self.assertEqual(resp.status_code, 400)

    def test_highscore_post_without_previous_play(self):
        """Tests if the high score gets updated when there is no previous score."""

        with self.client as client:
            resp = client.post("/game/highscore", json={"points": 4})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session[self.SESSION_KEY_GAMES_PLAYED], 1)
            self.assertEqual(session[self.SESSION_KEY_HIGH_SCORE], 4)
            self.assertEqual(resp.json[self.JSON_KEY_HIGHSCORE], 4)

    def test_zero_score_post_without_previous_play(self):
        """Tests if the high score remains zero when there is no previous score and the submitted score is zero."""

        with self.client as client:
            resp = client.post("/game/highscore", json={"points": 0})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session[self.SESSION_KEY_GAMES_PLAYED], 1)
            self.assertEqual(session[self.SESSION_KEY_HIGH_SCORE], 0)
            self.assertEqual(resp.json[self.JSON_KEY_HIGHSCORE], 0)

    def test_new_highscore_post_with_previous_play(self):
        """Tests if the high score gets updated when there is a new higher score."""

        with self.client as client:
            self.set_data(client, 3, 3)

            resp = client.post("/game/highscore", json={"points": 10})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session[self.SESSION_KEY_GAMES_PLAYED], 4)
            self.assertEqual(session[self.SESSION_KEY_HIGH_SCORE], 10)
            self.assertEqual(resp.json[self.JSON_KEY_HIGHSCORE], 10)

    def test_highscore_post_for_low_score_with_previous_play(self):
        """Tests if the high score remains the same when the submitted score is lower."""

        with self.client as client:
            self.set_data(client, 6, 10)

            resp = client.post("/game/highscore", json={"points": 4})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session[self.SESSION_KEY_GAMES_PLAYED], 7)
            self.assertEqual(session[self.SESSION_KEY_HIGH_SCORE], 10)
            self.assertEqual(resp.json[self.JSON_KEY_HIGHSCORE], 10)

    def test_highscore_post_for_zero_points_with_previous_play(self):
        """Tests if the high score remains the same when the submitted score is zero."""

        with self.client as client:
            self.set_data(client, 2, 10)

            resp = client.post("/game/highscore", json={"points": 0})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session[self.SESSION_KEY_GAMES_PLAYED], 3)
            self.assertEqual(session[self.SESSION_KEY_HIGH_SCORE], 10)
            self.assertEqual(resp.json[self.JSON_KEY_HIGHSCORE], 10)

    def test_highscore_post_for_negative_points(self):
        """Tests for a 400 response code if the submitted score is negative."""

        with self.client as client:
            self.set_data(client, 1, 0)

            resp = client.post("/game/highscore", json={"points": -3})

            self.assertEqual(resp.status_code, 400)
            self.assertEqual(session[self.SESSION_KEY_GAMES_PLAYED], 1)
            self.assertEqual(session[self.SESSION_KEY_HIGH_SCORE], 0)

    def test_highscore_post_for_no_points_are_passed(self):
        """Tests for a 400 response code if no score data is passed to the server."""

        with self.client as client:
            self.set_data(client, 1, 0)

            resp = client.post("/game/highscore")

            self.assertEqual(resp.status_code, 400)
            self.assertEqual(session[self.SESSION_KEY_GAMES_PLAYED], 1)
            self.assertEqual(session[self.SESSION_KEY_HIGH_SCORE], 0)

    # ==================================================

    def save_board_to_session(self, client):
        """Helper method to create a sample test board and save it to the Flask session."""

        with client.session_transaction() as change_session:
            change_session["board"] = [
                ["A", "A", "A", "A", "A"],
                ["A", "A", "A", "A", "A"],
                ["C", "A", "A", "A", "A"],
                ["A", "A", "A", "A", "A"],
                ["T", "A", "A", "A", "A"],
            ]

    def set_data(self, client, games_played, high_score):
        """Helper method to save other data, such as high score, into the Flask session."""

        with client.session_transaction() as change_session:
            change_session[self.SESSION_KEY_GAMES_PLAYED] = games_played
            change_session[self.SESSION_KEY_HIGH_SCORE] = high_score
