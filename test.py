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

            self.assertIn("<form>", html)
            self.assertIn('name="word"', html)
