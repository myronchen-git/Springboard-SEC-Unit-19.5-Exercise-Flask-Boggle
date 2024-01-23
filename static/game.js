class Game {
  static $guessResult = $("#guess-result");
  static $guessInput = $("#form-guess-word__input-guessed-word");
  static $timer = $("#timer");

  constructor({ timer = 60 } = {}) {
    $("#form-guess-word").submit(this.handleSubmit.bind(this));

    this.points = 0;
    this.foundWords = new Set();

    this.isEnabled = true;
    Game.$timer.text(timer);
    this.startTimer(timer);
  }

  /**
   * Gets the guessed word, passes it to a method that makes a HTTP request to the server, and displays the result on the
   * webpage.
   *
   * @param {Event} e The form submit event for guessing a word.
   */
  async handleSubmit(e) {
    e.preventDefault();

    if (this.isEnabled) {
      const word = Game.$guessInput.val();
      const result = await this.checkWord(word);

      if (result === "ok" && !this.acceptSubmittedWord(word)) {
        Game.$guessResult.text("already scored");
      } else {
        Game.$guessResult.text(result);
      }

      $("#points").text(this.points);
    } else {
      alert("Game Over!  You can not guess any more words.");
    }

    Game.$guessInput.val("");
  }

  /**
   * Calls the server to check if a word exists and if it is on the game board.  Returns the server response, which
   * should be a String that describes the validity.
   *
   * @param {String} word The submitted guessed word to check.
   */
  async checkWord(word) {
    try {
      const response = await axios.get("/game/guess", { params: { word } });
      return response.data.result.replaceAll("-", " ");
    } catch (e) {
      if (e.code === "ERR_BAD_REQUEST") {
        console.log(
          `status: ${e.response.status}\nstatusText: ${e.response.statusText}\ndata: ${e.response.data}`
        );
      } else {
        console.log("Error when contacting /game/guess.");
      }
    }
  }

  /**
   * Puts a valid word into a data structure for keeping track of submitted words and increases points.
   *
   * @param {String} word A valid word
   * @returns true if the word has not been submitted before.
   */
  acceptSubmittedWord(word) {
    if (!this.foundWords.has(word)) {
      this.foundWords.add(word);
      this.points += word.length;
      return true;
    } else {
      return false;
    }
  }

  /**
   * Starts a timer that will countdown and display the amount of seconds that are left in the game.
   *
   * @param {Number} seconds The amount of seconds before the game ends.
   */
  startTimer(seconds) {
    const intervalObj = setInterval(() => {
      seconds -= 1;
      Game.$timer.text(seconds);
      if (seconds <= 0) {
        clearInterval(intervalObj);
        this.endGame();
      }
    }, 1000);
  }

  async endGame() {
    this.isEnabled = false;
    const response = await axios.post("/game/highscore", {
      points: this.points,
    });
    $("#high-score").text(response.data.highScore);
  }
}

$(function () {
  new Game({ timer: 20 });
});
