# Boggle

The main purpose of this project is to practice writing Flask 
integration tests, but it has expanded to a well-made Boggle game. It 
contains both the front-end and back-end portions.

Users will land on a start page when reaching the root path. The start 
page allows users to configure the size of the game board and how long 
the timer lasts. Upon clicking the "Start" button, users will be sent 
to the game webpage, with the game board of letters, info on number of 
games played, info on the high score so far, timer, and current amount 
of points obtained in the current game session. Data is saved in a 
browser cookie, so data like high score is only from the user.

Users then submit a word through the webpage, the webpage contacts the 
back-end server, the server verifies if it is valid, the server sends 
back a result to the webpage, the webpage informs the user if the word 
is valid, and the current game points is updated.

This project was developed using the Python virtual environment.  Tests 
were done by utilizing the Flask test client, Flask Debug Toolbar, and 
Python assertions for the Python side of the code; and browser 
developer tools for the JavaScript, HTML, and CSS side.

---

Tools used:
* Python 3.12
* Flask 1.1.1
* Flask-DebugToolbar 0.11.0
* Jinja2 2.10.3
* HTML 5
* JavaScript ECMAScript 2018
* JQuery 3.7.1
* Bootstrap 5.3.2
