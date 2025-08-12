import streamlit as st
import json
import os
import random
import uuid
import pandas as pd

# --- Configuration ---
st.set_page_config(
    page_title="PyFlash: Python Flashcards",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Constants ---
FILE_PATH = "flashcards.json"
TOPICS = ["General", "Data Structures", "Functions", "OOP", "Algorithms", "Libraries"]

# --- Data Persistence Functions ---
def load_cards():
    """Loads flashcards from the JSON file."""
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_cards(cards):
    """Saves flashcards to the JSON file."""
    with open(FILE_PATH, "w") as f:
        json.dump(cards, f, indent=4)

# --- Session State Initialization ---
def initialize_session_state():
    """Initializes session state variables."""
    if 'cards' not in st.session_state:
        st.session_state.cards = load_cards()
    
    # Updated practice_session state
    if 'practice_session' not in st.session_state:
        st.session_state.practice_session = {
            "active": False,
            "shuffled_indices": [],
            "current_index": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "answer_submitted": False, # New state to track if user has submitted an answer
            "user_answer": "",       # New state to hold the user's submitted answer
            "last_answer_correct": None # New state for feedback
        }

initialize_session_state()

# --- UI Functions ---

def display_manage_page():
    """UI for managing flashcards (Add, Edit, Delete)."""
    st.header("🗂️ Manage Flashcards")
    st.write("Add, edit, or delete your Python flashcards here.")

    # --- Add New Card Expander ---
    with st.expander("➕ Add a New Flashcard", expanded=False):
        with st.form("new_card_form", clear_on_submit=True):
            question = st.text_area("❓ Question", placeholder="e.g., What is a Python list comprehension?")
            answer_type = st.radio("Answer Type", ["Text", "Code"], horizontal=True)
            if answer_type == "Code":
                answer = st.text_area("🔡 Code Answer", placeholder="e.g., [x**2 for x in range(10)]", height=200, key="code_answer")
            else:
                answer = st.text_area("🔡 Text Answer", placeholder="e.g., A concise way to create lists.", height=150, key="text_answer")
            topic = st.selectbox("🏷️ Topic", options=TOPICS)
            submitted = st.form_submit_button("Add Card")

            if submitted and question and answer:
                new_card = {
                    "id": str(uuid.uuid4()),
                    "question": question,
                    "answer": answer,
                    "is_code": (answer_type == "Code"),
                    "topic": topic,
                    "correct_count": 0,
                    "incorrect_count": 0
                }
                st.session_state.cards.append(new_card)
                save_cards(st.session_state.cards)
                st.toast("✅ Card added successfully!", icon="🎉")
                st.balloons()
            elif submitted:
                st.warning("Please fill in both the question and answer.")

    st.markdown("---")
    st.subheader("Your Card Collection")

    if not st.session_state.cards:
        st.info("You haven't added any flashcards yet. Add one above to get started! ☝️")
        return

    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search Cards", placeholder="Search by question or answer...")
    with col2:
        filter_topic = st.selectbox("Filter by Topic", ["All"] + TOPICS)

    filtered_cards = [
        card for card in st.session_state.cards
        if (search_query.lower() in card['question'].lower() or search_query.lower() in card['answer'].lower())
        and (filter_topic == "All" or card['topic'] == filter_topic)
    ]

    for i in range(0, len(filtered_cards), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(filtered_cards):
                card = filtered_cards[i + j]
                with cols[j]:
                    with st.container(border=True):
                        st.markdown(f"**Q:** {card['question']}")
                        st.markdown(f"**Topic:** `{card['topic']}`")

                        with st.expander("View/Edit Answer"):
                            st.code(card['answer'], language='python') if card['is_code'] else st.write(card['answer'])
                            if st.button("✏️ Edit", key=f"edit_{card['id']}"):
                                st.session_state.editing_card_id = card['id']
                            if st.session_state.get('editing_card_id') == card['id']:
                                with st.form(key=f"edit_form_{card['id']}"):
                                    edited_question = st.text_area("Edit Question", value=card['question'])
                                    edited_answer = st.text_area("Edit Answer", value=card['answer'], height=150)
                                    edited_topic = st.selectbox("Edit Topic", options=TOPICS, index=TOPICS.index(card['topic']))
                                    col_save, col_cancel = st.columns(2)
                                    if col_save.form_submit_button("💾 Save"):
                                        for idx, c in enumerate(st.session_state.cards):
                                            if c['id'] == card['id']:
                                                st.session_state.cards[idx]['question'] = edited_question
                                                st.session_state.cards[idx]['answer'] = edited_answer
                                                st.session_state.cards[idx]['topic'] = edited_topic
                                                break
                                        save_cards(st.session_state.cards)
                                        st.session_state.editing_card_id = None
                                        st.rerun()
                                    if col_cancel.form_submit_button("❌ Cancel"):
                                        st.session_state.editing_card_id = None
                                        st.rerun()

                        if st.button("🗑️ Delete", key=f"del_{card['id']}", type="primary"):
                            st.session_state.cards = [c for c in st.session_state.cards if c['id'] != card['id']]
                            save_cards(st.session_state.cards)
                            st.toast(f"🗑️ Card '{card['question'][:20]}...' deleted.", icon="🔥")
                            st.rerun()

# --- [MODIFIED] Practice Page ---
def display_practice_page():
    """UI for the interactive practice session with user input."""
    st.header("🎓 Practice Session")
    
    if not st.session_state.cards:
        st.warning("You have no cards to practice with. Please add some in the 'Manage Flashcards' section.")
        return

    session = st.session_state.practice_session

    if session["active"]:
        # --- Active Session Logic ---
        if st.button("⏹️ End Session"):
            session["active"] = False
            st.rerun()

        progress = (session["current_index"]) / len(session["shuffled_indices"])
        st.progress(progress, text=f"Card {session['current_index'] + 1} of {len(session['shuffled_indices'])}")

        card_idx = session["shuffled_indices"][session["current_index"]]
        card = session["cards_in_session"][card_idx]

        st.info(f"**Topic:** {card['topic']}")
        with st.container(border=True):
            st.markdown(f"### **Q:** {card['question']}")

        if not session["answer_submitted"]:
            with st.form("answer_form"):
                user_answer = st.text_area("Your Answer:", height=150)
                submitted = st.form_submit_button("Submit Answer", use_container_width=True)

                if submitted:
                    user_ans_norm = " ".join(user_answer.lower().strip().split())
                    correct_ans_norm = " ".join(card['answer'].lower().strip().split())
                    
                    session["user_answer"] = user_answer
                    session["answer_submitted"] = True
                    session["last_answer_correct"] = (user_ans_norm == correct_ans_norm)
                    st.rerun()
        else: 
            is_correct = session["last_answer_correct"]
            if is_correct:
                st.success("✅ Correct! Great job!", icon="🎉")
                with st.container(border=True):
                    st.markdown("#### Correct Answer:")
                    if card['is_code']:
                        st.code(card['answer'], language='python')
                    else:
                        st.write(card['answer'])
            else:
                st.error("❌ Not quite. Here's a comparison:", icon="🤔")
                col1, col2 = st.columns(2)
                with col1:
                    with st.container(border=True):
                        st.markdown("#### Your Answer:")
                        st.write(session["user_answer"])
                with col2:
                    with st.container(border=True):
                        st.markdown("#### Correct Answer:")
                        if card['is_code']:
                            st.code(card['answer'], language='python')
                        else:
                            st.write(card['answer'])

            if st.button("➡️ Next Card", use_container_width=True, type="primary"):
                handle_next_card(is_correct)
                st.rerun()
    else:
        # --- Session is NOT active. Show summary if it just ended, then show start button. ---
        if session['correct_answers'] > 0 or session['incorrect_answers'] > 0:
            st.balloons()
            st.success("🎉 You've completed the session!")
            display_session_summary()
            st.markdown("---")

        st.subheader("Ready to start a new session?")
        topic_to_practice = st.selectbox("Choose a topic to practice", ["All"] + TOPICS)
        
        if st.button("🚀 Start New Session!", type="primary", use_container_width=True):
            cards_to_practice = [card for card in st.session_state.cards if topic_to_practice == "All" or card['topic'] == topic_to_practice]
            
            if not cards_to_practice:
                st.error(f"No cards found for the topic '{topic_to_practice}'.")
                return

            indices = list(range(len(cards_to_practice)))
            random.shuffle(indices)
            
            # Reset session state for a new session
            initialize_session_state()
            session = st.session_state.practice_session
            session["active"] = True
            session["cards_in_session"] = cards_to_practice
            session["shuffled_indices"] = indices
            st.rerun()

def handle_next_card(was_correct):
    """Updates stats and moves to the next card."""
    session = st.session_state.practice_session
    card_idx = session["shuffled_indices"][session["current_index"]]
    card_id_to_update = session["cards_in_session"][card_idx]['id']

    # Update stats for the specific card in the main card list
    for i, c in enumerate(st.session_state.cards):
        if c['id'] == card_id_to_update:
            if was_correct:
                st.session_state.cards[i]['correct_count'] += 1
            else:
                st.session_state.cards[i]['incorrect_count'] += 1
            break
    save_cards(st.session_state.cards)

    # Update session stats
    if was_correct:
        session["correct_answers"] += 1
    else:
        session["incorrect_answers"] += 1
    
    # Move to the next card or end the session
    if session["current_index"] + 1 < len(session["shuffled_indices"]):
        session["current_index"] += 1
        session["answer_submitted"] = False
        session["user_answer"] = ""
        session["last_answer_correct"] = None
    else:
        # Session is over. Just set it to inactive.
        # The main page will handle displaying the summary.
        session["active"] = False

def display_session_summary():
    """Shows a summary after a practice session ends."""
    session = st.session_state.practice_session
    st.subheader("Session Summary")
    col1, col2 = st.columns(2)
    col1.metric("Correct Answers ✅", session['correct_answers'])
    col2.metric("Incorrect Answers ❌", session['incorrect_answers'])

def display_stats_page():
    """UI for displaying learning statistics."""
    st.header("📊 Your Learning Statistics")

    if not st.session_state.cards:
        st.info("No data to display. Complete a practice session to see your stats.")
        return

    cards_df = pd.DataFrame(st.session_state.cards)

    st.subheader("Overall Performance")
    total_correct = cards_df['correct_count'].sum()
    total_incorrect = cards_df['incorrect_count'].sum()
    total_attempts = total_correct + total_incorrect

    if total_attempts == 0:
        st.write("You haven't attempted any cards yet in a practice session.")
    else:
        accuracy = (total_correct / total_attempts) * 100
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cards", len(cards_df))
        col2.metric("Total Correct Answers", f"{total_correct}")
        col3.metric("Overall Accuracy", f"{accuracy:.2f}%")

    st.markdown("---")
    st.subheader("Card Distribution by Topic")
    topic_counts = cards_df['topic'].value_counts()
    st.bar_chart(topic_counts)

    st.markdown("---")
    st.subheader("Your Most Challenging Cards")
    difficult_cards = cards_df.sort_values(by='incorrect_count', ascending=False).head(5)
    difficult_cards = difficult_cards[difficult_cards['incorrect_count'] > 0]

    if difficult_cards.empty:
        st.write("Great job! No challenging cards identified yet.")
    else:
        for _, row in difficult_cards.iterrows():
            st.error(f"**Q: {row['question']}** (Incorrect: {row['incorrect_count']} times)")

# --- Main App Logic ---
st.sidebar.title("PyFlash 🧠")
st.sidebar.markdown("Your personal Python flashcard application.")
page = st.sidebar.radio(
    "Navigation",
    ["🎓 Practice Session", "🗂️ Manage Flashcards", "📊 Statistics"],
    captions=["Test yourself", "Add & Edit Cards", "View Your Progress"]
)
st.sidebar.markdown("---")
st.sidebar.info("Created with ❤️ using Streamlit.")

if page == "🗂️ Manage Flashcards":
    display_manage_page()
elif page == "🎓 Practice Session":
    display_practice_page()
elif page == "📊 Statistics":
    display_stats_page()