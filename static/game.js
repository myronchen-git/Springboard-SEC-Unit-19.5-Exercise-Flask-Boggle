class Game {
  constructor() {
    $("#form-guess-word").submit(this.handleSubmit.bind(this));
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
    $("#guess-result").text(result);
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
}

$(function () {
  new Game();
});
