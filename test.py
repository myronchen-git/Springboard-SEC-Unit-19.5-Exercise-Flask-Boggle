import string
from unittest import TestCase

from flask import session

from app import app
from boggle import Boggle

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


class FlaskTests(TestCase):
    """Tests for the game."""

    def test_root_redirect(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/game")

    def test_board_creation(self):
        with app.test_client() as client:
            resp = client.get("/game")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("<table>", html)
            self.assertIn("<tr>", html)
            self.assertIn("<td>", html)

    def test_board_saving_in_session(self):
        with app.test_client() as client:
            resp = client.get("/game")

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(len(session["board"]), 5)
            self.assertEqual(len(session["board"][0]), 5)
            self.assertIn(session["board"][0][0], string.ascii_uppercase)

    def test_form_creation(self):
        with app.test_client() as client:
            resp = client.get("/game")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("</form>", html)
            self.assertIn('name="guessed-word"', html)

    def test_header_creation(self):
        with app.test_client() as client:
            resp = client.get("/game")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("Points", html)
            self.assertIn('id="points"', html)

    def test_word_submission(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [
                    ["A", "A", "A", "A", "A"],
                    ["A", "A", "A", "A", "A"],
                    ["C", "A", "A", "A", "A"],
                    ["A", "A", "A", "A", "A"],
                    ["T", "A", "A", "A", "A"],
                ]

            resp = client.get("/game/guess?word=zzzz")
            self.assertEqual(resp.json["result"], "not-a-word")

            resp = client.get("/game/guess?word=zoozoo")
            self.assertEqual(resp.json["result"], "not-on-board")

            resp = client.get("/game/guess?word=cat")
            self.assertEqual(resp.json["result"], "ok")

            resp = client.get("/game/guess?word=555")
            self.assertEqual(resp.json["result"], "not-a-word")
