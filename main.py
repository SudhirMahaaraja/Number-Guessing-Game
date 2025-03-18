import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
import plotly.express as px
import string


# Initialize MongoDB connection
def init_db():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['number_game_db']
        collection = db['scores']
        # Test the connection
        client.server_info()  # This will raise an exception if connection fails
        return collection
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None


# Save score to MongoDB
def save_score(name, guesses, time_taken, collection):
    # Calculate score (lower is better)
    # Formula: (guesses * 10) + (time_taken / 5)
    score = (guesses * 10) + (time_taken / 5)

    try:
        collection.insert_one({
            'name': name,
            'guesses': guesses,
            'time_taken': time_taken,
            'score': score,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        st.error(f"Error saving score: {e}")


# Get top 5 scores
def get_top_scores(collection):
    try:
        cursor = collection.find().sort('score', 1).limit(5)
        return pd.DataFrame(list(cursor))
    except Exception as e:
        st.error(f"Error getting scores: {e}")
        return pd.DataFrame()


# Generate a random 4-digit number with no duplicates
def generate_number():
    digits = random.sample(range(10), 4)
    return ''.join(map(str, digits))


# Evaluate guess and return feedback
def evaluate_guess(secret_number, guess):
    plus = 0
    minus = 0

    for i in range(4):
        if guess[i] == secret_number[i]:
            plus += 1
        elif guess[i] in secret_number:
            minus += 1

    return '+' * plus + '-' * minus


# Generate random encouraging messages
def get_encouragement():
    messages = [
        "You're getting closer! 💪",
        "Keep going! 🚀",
        "You've got this! 🌟",
        "Almost there! 🏆",
        "Don't give up now! 🔍",
        "You're doing great! 🎯",
        "One step closer! 🧩",
        "Your next guess could be it! 🍀",
        "Keep those digits coming! 🔢",
        "You're on fire! 🔥"
    ]
    return random.choice(messages)


# Generate a fun fact about numbers
def get_number_fact():
    facts = [
        "The fear of the number 13 is called triskaidekaphobia.",
        "The number 4 is considered unlucky in many East Asian cultures.",
        "Zero was invented as a number in India by mathematician Aryabhata.",
        "Pi (π) has been calculated to over 31 trillion digits.",
        "The most common lucky number across cultures is 7.",
        "All odd numbers have the letter 'e' in their spelling in English.",
        "A googol is the number 1 followed by 100 zeros.",
        "The number 42 is considered the 'Answer to the Ultimate Question of Life, the Universe, and Everything' in Hitchhiker's Guide to the Galaxy.",
        "123454321 is a palindromic number that forms a pyramid shape when written in sequence.",
        "The Golden Ratio (approximately 1.618) appears frequently in nature."
    ]
    return random.choice(facts)


# Generate confetti animation characters for winning
def generate_confetti():
    confetti_chars = "🎉✨🎊🎇🎆👏🥳"
    return ''.join(random.choices(confetti_chars, k=50))


# Generate fun number reveal animation (simple ASCII art)
def reveal_number_animation(number):
    frames = []
    chars = string.punctuation + string.ascii_letters

    # Create 5 frames of "noise" gradually revealing the number
    for i in range(5):
        frame = ""
        for digit in number:
            if random.random() < i / 4:  # Gradually increase chance of showing real digit
                frame += digit
            else:
                frame += random.choice(chars)
        frames.append(frame)

    # Add the final correct number
    frames.append(number)

    return frames


# Main game function
def main():
    # Initialize database connection
    db_connection_successful = True
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['number_game_db']
        collection = db['scores']
        # Test the connection
        client.server_info()  # This will raise an exception if connection fails
    except Exception as e:
        db_connection_successful = False
        st.error(f"Failed to connect to MongoDB. Please make sure MongoDB is running on localhost:27017. Error: {e}")
        collection = None

    # Set title and page config
    st.set_page_config(page_title="Number Guessing Game", page_icon="🎮")

    # Fun title with emoji
    st.markdown("# 🔢 Guessing Number Game 🎲")

    # Only continue with the game if we have a database connection
    if not db_connection_successful:
        st.warning("Game will run in demo mode without score saving.")

    # Display a random number fact in the sidebar
    st.sidebar.markdown("### Fun Number Fact")
    if 'number_fact' not in st.session_state:
        st.session_state.number_fact = get_number_fact()
    st.sidebar.info(st.session_state.number_fact)
    if st.sidebar.button("New Fun Fact"):
        st.session_state.number_fact = get_number_fact()
        st.rerun()

    # Initialize session state
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = ""
    if 'guesses' not in st.session_state:
        st.session_state.guesses = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'player_name' not in st.session_state:
        st.session_state.player_name = ""
    if 'reveal_frames' not in st.session_state:
        st.session_state.reveal_frames = []
    if 'reveal_index' not in st.session_state:
        st.session_state.reveal_index = 0
    if 'showing_reveal' not in st.session_state:
        st.session_state.showing_reveal = False

    # Game controls
    col1, col2 = st.columns([1, 4])

    with col1:
        if not st.session_state.game_active and not st.session_state.showing_reveal:
            if st.button("🎮 Start New Game", use_container_width=True):
                st.session_state.game_active = "name_input"
                st.rerun()

    # Name input
    if st.session_state.game_active == "name_input":
        st.markdown("### Enter Your Name")
        name = st.text_input("", placeholder="Your Name", key="name_input")
        if st.button("🚀 Start Game", use_container_width=True) and name:
            st.session_state.player_name = name
            st.session_state.secret_number = generate_number()
            st.session_state.guesses = 0
            st.session_state.start_time = time.time()
            st.session_state.history = []
            st.session_state.game_active = True
            st.rerun()

    # Number reveal animation
    if st.session_state.showing_reveal:
        st.markdown("### 🎭 Revealing Secret Number")
        reveal_container = st.empty()

        # Display current frame
        if st.session_state.reveal_index < len(st.session_state.reveal_frames):
            reveal_container.markdown(f"## {st.session_state.reveal_frames[st.session_state.reveal_index]}")
            st.session_state.reveal_index += 1
            time.sleep(0.5)
            st.rerun()
        else:
            reveal_container.markdown(f"## The secret number was: {st.session_state.secret_number} 🎯")
            if st.button("Play Again", use_container_width=True):
                st.session_state.showing_reveal = False
                st.session_state.game_active = False
                st.rerun()

    # Active game
    elif st.session_state.game_active == True:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### Player: {st.session_state.player_name} 👤")
            st.markdown(f"### Guesses: {st.session_state.guesses} 🎯")

            # Calculate elapsed time
            elapsed = time.time() - st.session_state.start_time
            st.markdown(f"### Time: {elapsed:.1f} seconds ⏱️")

        with col2:
            # Display a random encouragement message that changes every few guesses
            if st.session_state.guesses > 0 and st.session_state.guesses % 3 == 0:
                st.info(get_encouragement())

        # Game input
        st.markdown("### Enter your guess:")
        guess = st.text_input(
            "",
            placeholder="Enter 4 digits with no duplicates",
            key="guess_input",
            max_chars=4
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Submit Guess", use_container_width=True):
                if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
                    st.error("Please enter a valid 4-digit number with no duplicate digits.")
                else:
                    st.session_state.guesses += 1
                    result = evaluate_guess(st.session_state.secret_number, guess)

                    # Record this guess in history
                    st.session_state.history.append({
                        "guess": guess,
                        "result": result,
                        "guess_number": st.session_state.guesses,
                        "time": time.time() - st.session_state.start_time
                    })

                    # Check if the guess is correct
                    if result == "++++" or guess == st.session_state.secret_number:
                        time_taken = time.time() - st.session_state.start_time

                        # Save score if we have database connection
                        if db_connection_successful and collection is not None:
                            save_score(st.session_state.player_name, st.session_state.guesses, time_taken, collection)

                        st.success(
                            f"🎉 Congratulations! You guessed the number in {st.session_state.guesses} attempts! 🎉")
                        st.balloons()
                        st.markdown(generate_confetti())
                        st.markdown(f"### Time taken: {time_taken:.2f} seconds")
                        st.session_state.game_active = False

                    st.rerun()

        with col2:
            if st.button("🏳️ Give Up", use_container_width=True):
                st.session_state.showing_reveal = True
                st.session_state.reveal_frames = reveal_number_animation(st.session_state.secret_number)
                st.session_state.reveal_index = 0
                st.session_state.game_active = False
                st.rerun()

        # Display guess history
        if st.session_state.history:
            st.markdown("### Guess History")

            # Create a dataframe for display
            history_df = pd.DataFrame(st.session_state.history)

            # Show as a table
            st.table(history_df[["guess_number", "guess", "result"]])

            # Visualize guesses with a chart
            if len(history_df) > 1:
                st.markdown("### Your Progress")
                # Count plus signs in result to track correct digits
                history_df['correct_digits'] = history_df['result'].apply(lambda x: x.count('+'))

                fig = px.line(
                    history_df,
                    x="guess_number",
                    y="correct_digits",
                    title="Correct Digits by Guess",
                    markers=True
                )
                fig.update_layout(xaxis_title="Guess Number", yaxis_title="Correct Digits")
                st.plotly_chart(fig, use_container_width=True)

    # Display leaderboard only if we have database connection
    if db_connection_successful and collection is not None:
        st.markdown("## 🏆 Leaderboard - Top 5 Scores")
        top_scores = get_top_scores(collection)
        if not top_scores.empty and '_id' in top_scores:
            # Format the data for display
            display_df = top_scores.copy()
            # Only keep necessary columns and rename them
            display_df = display_df.drop('_id', axis=1)

            display_df['time_taken'] = display_df['time_taken'].apply(lambda x: f"{x:.2f} seconds")
            display_df['score'] = display_df['score'].apply(lambda x: f"{x:.2f}")

            # Add medals for top 3
            if len(display_df) >= 1:
                display_df.loc[0, 'name'] = display_df.loc[0, 'name'] + " 🥇"
            if len(display_df) >= 2:
                display_df.loc[1, 'name'] = display_df.loc[1, 'name'] + " 🥈"
            if len(display_df) >= 3:
                display_df.loc[2, 'name'] = display_df.loc[2, 'name'] + " 🥉"

            st.table(display_df)

            # Add explanation of scoring
            #st.info("🧮 Score Formula: (guesses × 10) + (time_taken ÷ 5) | Lower is better!")
        else:
            st.info("No scores yet! Be the first to make the leaderboard! 🏆")
    else:
        st.info("⚠️ Leaderboard is unavailable in demo mode (MongoDB not connected)")

    # Show rules
    with st.expander("📋 Game Rules"):
        st.write("""
        1. The computer selects a random 4-digit number with no duplicate digits.
        2. You need to guess this number in as few attempts as possible.
        3. After each guess, you'll receive feedback:
           - '+' means a digit is correct and in the right position
           - '-' means a digit is correct but in the wrong position
        4. Example: If the secret number is 1234 and you guess 1672, you'll get '+−' 
           (+ for 1 in the correct position, - for 2 in the wrong position)
        5. Your score is calculated based on the number of guesses and time taken.
           Lower scores are better!
        """)

    # Tips for new players
    with st.expander("💡 Pro Tips"):
        st.write("""
        - Start with digits spread across the range (e.g., 1592)
        - When you get a '+', keep that digit in the same position in future guesses
        - When you get a '-', try moving that digit to different positions
        - Process of elimination is key - track which digits are NOT in the number
        - Try to optimize both speed and number of guesses for the best score
        """)


if __name__ == "__main__":
    main()