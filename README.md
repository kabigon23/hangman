# Hangman 1.0

A simple graphical Hangman game built using PyQt5. In this game, you guess letters to figure out a hidden word, with only a limited number of incorrect guesses before the full hangman is drawn.

## Features

- Reads random words from `words.txt` for the word to guess
- Displays scaffold and hangman parts as mistakes are made
- Letter buttons for guessing, deactivates after selection
- Displays current status of the guessed word
- Restart button to start a new game, Quit button to exit
- "Game Over" message when all attempts are used

## Requirements

- Python 3.x
- PyQt5

## Installation

1. Clone this repository:
   ```bash
   git clone "https://github.com/kabigon23/hangman.git"
   ```
2. Navigate into the project directory:
   ```bash
   cd hangman
   ```
3. Install the required packages:
   ```bash
   pip install PyQt5
   ```

## Running the Game

1. Ensure you have a `words.txt` file in the same directory as the script, containing words for the game.
2. Run the main Python file:
   ```bash
   python hangman.py
   ```

## How to Play

1. A word is randomly selected from `words.txt`, and you need to guess it letter by letter.
2. Click on the letter buttons to make guesses. Correct guesses will reveal the letters in the word, while incorrect guesses will draw parts of the hangman.
3. You have 6 attempts to guess the word before the hangman is fully drawn.
4. Click "Restart" to play a new game or "Quit" to exit.

## License

This project is open source and available under the [MIT License](LICENSE).
