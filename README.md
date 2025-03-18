# Number-Guessing-Game
Interactive 4-digit guessing game with animations, leaderboard, and MongoDB scoring. Play &amp; enjoy!

## Overview
This project is a web-based interactive guessing game built using Streamlit. In the game, a player is prompted to enter their name and then guess a randomly generated 4-digit number with unique digits. For each guess, the game provides immediate feedback using:
- **"+"** for a digit that is correct and in the correct position.
- **"-"** for a digit that is correct but in the wrong position.

The game tracks the number of guesses and the time taken, saves scores to a MongoDB database, and displays a leaderboard. Additional features include fun number facts, confetti animations, reveal animations, and dynamic progress charts to enhance the user experience.

## Features
- **Interactive UI:** Developed with Streamlit for a seamless web interface.
- **Random Unique 4-Digit Number:** Ensures no duplicate digits using Python's random sampling.
- **Real-Time Feedback:** Provides '+' and '-' indicators for each guess.
- **Score Tracking:** Measures both guess count and elapsed time.
- **Leaderboard:** Displays top scores from MongoDB using a custom scoring formula.
- **Animations & Visual Effects:** Includes confetti on win, reveal animations, and interactive progress charts.
- **Fun Extras:** Offers random number facts and encouragement messages.

## Prerequisites
- **Python 3.6+**
- **MongoDB:** Ensure MongoDB is installed and running (default connection: `mongodb://localhost:27017/`).

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/Streamlit-Guessing-Game.git
   cd Streamlit-Guessing-Game
   ```
2. **Install Required Packages:**
   Install dependencies using pip:
   ```bash
   pip install streamlit pymongo pandas plotly
   ```

## Running the Application
To start the game locally, run:
```bash
streamlit run main.py
```

## Project Structure
- **main.py:** Contains the entire game logic, UI, and integration with MongoDB.
- **README.md:** This file.
- **requirements.txt (optional):** List of dependencies for easy installation.

## Configuration
- **MongoDB Connection:**  
  The app connects to a MongoDB instance on `localhost:27017`. If MongoDB is not running, the game will run in demo mode without saving scores.
- **Scoring Formula:**  
  The score is calculated as:  
  `(guesses * 10) + (time_taken / 5)`  
  Lower scores indicate better performance.

## How to Play
1. **Start a New Game:** Click the "Start New Game" button and enter your name.
2. **Guess the Number:** Input a 4-digit number with no repeated digits.
3. **Receive Feedback:** For each guess, the game shows:
   - **"+"** for digits in the correct position.
   - **"-"** for digits that exist but are in the wrong position.
4. **Win the Game:** When you guess the correct number, you'll see a congratulatory message, confetti animation, and your score will be saved.
5. **Give Up:** Click the "Give Up" button to reveal the secret number with an animated effect.
6. **Leaderboard:** View the top scores based on a mix of speed and guess count.

## Contributing
Contributions are welcome! Please feel free to fork the repository and submit pull requests. For major changes, open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements
- Built using [Streamlit](https://streamlit.io)
- Database powered by [MongoDB](https://www.mongodb.com)
- Visualizations using [Plotly](https://plotly.com)
