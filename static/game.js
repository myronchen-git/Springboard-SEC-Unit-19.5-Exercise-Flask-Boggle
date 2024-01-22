class Game {
  static $guessResult = $("#guess-result");

  constructor() {
    $("#form-guess-word").submit(this.handleSubmit.bind(this));

    this.points = 0;
    this.foundWords = new Set();
  }

  /**
   * Gets the guessed word, passes it to a method that makes a HTTP request to the server, and displays the result on the
   * webpage.
   *
   * @param {Event} e The form submit event for guessing a word.
   */
  async handleSubmit(e) {
    e.preventDefault();

    const word = $("#form-guess-word__input-guessed-word").val();
    const result = await this.checkWord(word);

    if (result === "ok" && !this.acceptSubmittedWord(word)) {
      Game.$guessResult.text("already scored");
    } else {
      Game.$guessResult.text(result);
    }

    $("#points").text(this.points);
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
      console.log("Error when contacting /game/guess.");
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
}

$(function () {
  new Game();
});
