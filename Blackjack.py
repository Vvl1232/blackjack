import streamlit as st
import random as rd

# Deal a card
def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    random_card = rd.choice(cards)
    return random_card

# Calculate the score
def calculate_score(cards):
    '''Take a list of cards and return the score calculated from the cards'''
    
    # Check for a blackjack (a hand with only 2 cards: ace + 10)
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    
    # Check for an ace. If the score is already over 21, remove the ace and add 1
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    
    return sum(cards)

# Display the rules and how to play the game
def about():
    st.header("About Blackjack Game 🎲🃏")
    st.write("""
    **Blackjack** is a popular card game where the goal is to get as close to 21 points as possible without exceeding it.
    
    **Rules:**
    - Number cards (2-10) are worth their face value.
    - Face cards (Jack, Queen, King) are worth 10 points.
    - Aces can be worth either 1 or 11 points, depending on which value helps the hand the most.
    - If a player’s hand exceeds 21 points, they bust and lose the game.
    
    **How to Play:**
    1. Both the player and the computer are dealt two cards initially.
    2. The player can see their own cards and one of the computer's cards.
    3. The player can choose to "hit" (take another card) or "stand" (end their turn).
    4. The goal is to get closer to 21 points than the computer without going over 21.
    5. The computer will also draw cards until it reaches at least 17 points or busts.
    6. The player wins if they get a higher score than the computer without busting.

    Enjoy the game and good luck! 🎉
    """)

# Streamlit app setup
st.title("Blackjack Game 🎲🃏")
st.write("Let's play a game of Blackjack!")
st.warning("Just keep your score higher than the computer's or as close to 21 as possible without exceeding it. Good luck! 🤞")

# Sidebar with navigation
option = st.sidebar.selectbox("Navigate", ["Game", "About"])

if option == "Game":
    if "user_cards" not in st.session_state:
        st.session_state.user_cards = []
    if "computer_cards" not in st.session_state:
        st.session_state.computer_cards = []
    if "is_game_over" not in st.session_state:
        st.session_state.is_game_over = False

    # Deal initial cards
    if not st.session_state.user_cards:
        for _ in range(2):
            st.session_state.user_cards.append(deal_card())
            st.session_state.computer_cards.append(deal_card())

    user_score = calculate_score(st.session_state.user_cards)
    computer_score = calculate_score(st.session_state.computer_cards)

    st.info(f"**Your cards:** {st.session_state.user_cards}, **current score:** {user_score}")
    st.info(f"**Computer's first card:** {st.session_state.computer_cards[0]} and second card's face is down!!! ")

    # User's turn
    if st.session_state.is_game_over:
        while computer_score != 0 and computer_score < 17:
            st.session_state.computer_cards.append(deal_card())
            computer_score = calculate_score(st.session_state.computer_cards)

        st.info(f"**Computer's final hand:** {st.session_state.computer_cards}, **final score:** {computer_score}")

        if user_score == 0:
            st.success("🎉 You win with a Blackjack! 🃏")
        elif computer_score == 0:
            st.error("💻 Computer wins with a Blackjack! 🃏")
        elif user_score > 21:
            st.error("🚨 You went over 21. You lose! 😢")
        elif computer_score > 21:
            st.success("🎉 Computer went over 21. You win! 🥳")
        elif user_score == computer_score:
            st.info("🤝 It's a draw! 😃")
        elif user_score > computer_score:
            st.success("🎉 You win! Great job! 💪")
        else:
            st.error("💻 Computer wins! Better luck next time! 🍀")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Get another card ➕"):
                st.session_state.user_cards.append(deal_card())
                user_score = calculate_score(st.session_state.user_cards)
                st.info(f"**Your cards:** {st.session_state.user_cards}, **current score:** {user_score}")
                if user_score > 21:
                    st.session_state.is_game_over = True

        with col2:
            if st.button("Pass 🛑"):
                with col1:
                    st.session_state.is_game_over = True

                    # Initiate computer's turn
                    while computer_score != 0 and computer_score < 17:
                        st.session_state.computer_cards.append(deal_card())
                        computer_score = calculate_score(st.session_state.computer_cards)

                    st.info(f"**Computer's final hand:** {st.session_state.computer_cards}, **final score:** {computer_score}")

                    if user_score == 0:
                        st.success("🎉 You win with a Blackjack! 🃏")
                    elif computer_score == 0:
                        st.error("💻 Computer wins with a Blackjack! 🃏")
                    elif user_score > 21:
                        st.error("🚨 You went over 21. You lose! 😢")
                    elif computer_score > 21:
                        st.success("🎉 Computer went over 21. You win! 🥳")
                    elif user_score == computer_score:
                        st.info("🤝 It's a draw! 😃")
                    elif user_score > computer_score:
                        st.success("🎉 You win! Great job! 💪")
                    else:
                        st.error("💻 Computer wins! Better luck next time! 🍀")

    # Reset the game
    if st.button("Reset Game 🔄"):
        st.session_state.user_cards = []
        st.session_state.computer_cards = []
        st.session_state.is_game_over = False
        st.rerun()
else:
    about()
