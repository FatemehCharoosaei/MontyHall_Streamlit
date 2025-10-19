import streamlit as st
import random
from main import monty_hall_game  # Importing the game logic from main.py
# Page configuration
st.set_page_config(
   page_title="Monty Hall Simulator",
   page_icon="🚗",
   layout="centered",
   initial_sidebar_state="collapsed"
)
# Custom CSS for styling
st.markdown("""
<style>
   .main {
       padding: 2rem;
   }
   .stButton>button {
       width: 100%;
       border-radius: 10px;
       padding: 10px;
       font-weight: bold;
       transition: all 0.3s ease;
   }
   .stButton>button:hover {
       transform: scale(1.05);
   }
   .result-box {
       border-radius: 15px;
       padding: 25px;
       margin: 20px 0;
       box-shadow: 0 4px 8px rgba(0,0,0,0.1);
   }
   .win-box {
       background: linear-gradient(145deg, #d4f4dd, #a8e6cf);
       border: 2px solid #28a745;
   }
   .lose-box {
       background: linear-gradient(145deg, #f8d7da, #ffaaa5);
       border: 2px solid #dc3545;
   }
   .stats-box {
       background: linear-gradient(145deg, #e9ecef, #f8f9fa);
       border-radius: 15px;
       padding: 20px;
       margin: 20px 0;
       box-shadow: 0 4px 8px rgba(0,0,0,0.1);
   }
   .header {
       text-align: center;
       color: #2c3e50;
       margin-bottom: 30px;
   }
   .door-button {
       font-size: 24px;
       height: 120px;
       margin: 10px;
   }
   .highlight {
       border: 3px solid #ff9900 !important;
       box-shadow: 0 0 15px #ff9900 !important;
   }
</style>
""", unsafe_allow_html=True)
# Initialize session state variables
if 'step' not in st.session_state:
   st.session_state.step = 0  # 0: door selection, 1: reveal goat, 2: decision, 3: show result
   st.session_state.initial_choice = None
   st.session_state.revealed_door = None
   st.session_state.user_decision = None  # Changed from 'switch' to avoid conflict
   st.session_state.result = None
   st.session_state.doors = [False, False, False]  # Track door states
   st.session_state.stats = {
       "wins_with_switch": 0,
       "total_with_switch": 0,
       "wins_without_switch": 0,
       "total_without_switch": 0
   }
# Header section
st.markdown("<h1 class='header'>🎯 Monty Hall Paradox Simulator</h1>", unsafe_allow_html=True)
st.markdown("### Choose a door and test your intuition about probability!")
# Function to reset the game without resetting stats
def reset_game():
   st.session_state.step = 0
   st.session_state.initial_choice = None
   st.session_state.revealed_door = None
   st.session_state.user_decision = None
   st.session_state.result = None
   st.session_state.doors = [False, False, False]
# Step 0: Initial door selection
if st.session_state.step == 0:
   st.markdown("### 🚪 Select one of the doors below:")
   
   # Create three door buttons
   col1, col2, col3 = st.columns(3)
   with col1:
       if st.button("🚪 Door 1", key="door1", use_container_width=True):
           st.session_state.initial_choice = 0
           st.session_state.step = 1
           st.rerun()
   with col2:
       if st.button("🚪 Door 2", key="door2", use_container_width=True):
           st.session_state.initial_choice = 1
           st.session_state.step = 1
           st.rerun()
   with col3:
       if st.button("🚪 Door 3", key="door3", use_container_width=True):
           st.session_state.initial_choice = 2
           st.session_state.step = 1
           st.rerun()
   
   st.markdown("---")
   st.info("ℹ️ Behind one door is a car 🚗, and behind the other two are goats 🐐. After you select a door, the host will reveal a goat behind one of the other doors.")
# Step 1: Reveal a goat behind one of the other doors
if st.session_state.step == 1:
   # Create the game scenario
   doors = ["goat", "goat", "car"]
   random.shuffle(doors)
   
   # Find a door to reveal (a goat that wasn't chosen)
   revealed_door = next(i for i in range(3) if i != st.session_state.initial_choice and doors[i] == "goat")
   st.session_state.revealed_door = revealed_door
   st.session_state.doors = doors
   
   st.markdown(f"### You selected Door {st.session_state.initial_choice + 1}")
   st.markdown(f"### The host opens Door {revealed_door + 1} to reveal a goat! 🐐")
   
   # Show the door visualization
   col1, col2, col3 = st.columns(3)
   door_labels = ["🚪 Door 1", "🚪 Door 2", "🚪 Door 3"]
   
   for i in range(3):
       with eval(f"col{i+1}"):
           if i == revealed_door:
               st.button("🐐 Goat Revealed", key=f"revealed_{i}", disabled=True, use_container_width=True)
           elif i == st.session_state.initial_choice:
               st.button(f"🚪 Your Choice", key=f"chosen_{i}", disabled=True, use_container_width=True)
           else:
               st.button(door_labels[i], key=f"other_{i}", disabled=True, use_container_width=True)
   
   st.markdown("### Now, what would you like to do?")
   st.markdown("Would you like to switch to the other unopened door or stick with your original choice?")
   
   # Decision buttons - using callback functions to avoid the key conflict
   col1, col2 = st.columns(2)
   
   def set_switch_true():
       st.session_state.user_decision = True
       st.session_state.step = 2
       
   def set_switch_false():
       st.session_state.user_decision = False
       st.session_state.step = 2
   
   with col1:
       st.button("🔄 Switch Doors", key="switch_btn", on_click=set_switch_true, use_container_width=True)
   with col2:
       st.button("⏹ Stay with Original Choice", key="stay_btn", on_click=set_switch_false, use_container_width=True)
# Step 2: Process the game result
if st.session_state.step == 2:
   # Run the game simulation
   win = monty_hall_game(switch_doors=st.session_state.user_decision)
   st.session_state.result = win
   
   # Update statistics
   if st.session_state.user_decision:
       st.session_state.stats["total_with_switch"] += 1
       if win:
           st.session_state.stats["wins_with_switch"] += 1
   else:
       st.session_state.stats["total_without_switch"] += 1
       if win:
           st.session_state.stats["wins_without_switch"] += 1
   
   st.session_state.step = 3
   st.rerun()
# Step 3: Display the final result
if st.session_state.step == 3:
   # Apply different styling based on win/lose
   result_class = "win-box" if st.session_state.result else "lose-box"
   
   st.markdown(f"<div class='result-box {result_class}'>", unsafe_allow_html=True)
   
   if st.session_state.user_decision:
       st.markdown("### 🔄 You decided to switch doors")
   else:
       st.markdown("### ⏹ You decided to stick with your original choice")
   
   if st.session_state.result:
       st.success("🎉 Congratulations! You won the car!")
       st.image("https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x0,y0,safe&width=1200",
                caption="🚗 Your new car!", use_container_width=True)
       st.balloons()
   else:
       st.error("😢 Sorry, you got a goat!")
       st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThohR4RKt2MfFr6jh3OjsMVi1gaSFS3SDY5w&s",
                caption="🐐 Better luck next time!", use_container_width=True)
   
   st.markdown("</div>", unsafe_allow_html=True)
   
   # Display statistics
   st.markdown("<div class='stats-box'>", unsafe_allow_html=True)
   st.markdown("### 📊 Your Statistics")
   
   col1, col2 = st.columns(2)
   with col1:
       if st.session_state.stats["total_with_switch"] > 0:
           switch_rate = (st.session_state.stats["wins_with_switch"] / st.session_state.stats["total_with_switch"]) * 100
           st.metric("Wins when switching", f"{st.session_state.stats['wins_with_switch']}/{st.session_state.stats['total_with_switch']}",
                    f"{switch_rate:.1f}% win rate")
       else:
           st.metric("Wins when switching", "0/0", "0% win rate")
   
   with col2:
       if st.session_state.stats["total_without_switch"] > 0:
           no_switch_rate = (st.session_state.stats["wins_without_switch"] / st.session_state.stats["total_without_switch"]) * 100
           st.metric("Wins when not switching", f"{st.session_state.stats['wins_without_switch']}/{st.session_state.stats['total_without_switch']}",
                    f"{no_switch_rate:.1f}% win rate")
       else:
           st.metric("Wins when not switching", "0/0", "0% win rate")
   
   st.markdown("</div>", unsafe_allow_html=True)
   
   # Play again button
   if st.button("🔁 Play Again", key="play_again", use_container_width=True):
       reset_game()
       st.rerun()
# Add explanation of the Monty Hall problem
with st.expander("ℹ️ Learn about the Monty Hall Paradox"):
   st.markdown("""
   ### The Monty Hall Problem
   
   The Monty Hall problem is a famous probability puzzle based on the American television game show *Let's Make a Deal*.
   
   **How it works:**
   1. You're presented with 3 doors. Behind one is a car 🚗, behind the other two are goats 🐐.
   2. You select a door.
   3. The host (who knows what's behind each door) opens one of the remaining doors, always revealing a goat.
   4. You're given a choice: stick with your original selection or switch to the other unopened door.
   
   **The Paradox:**
   - It seems like it shouldn't matter whether you switch or not (50/50 chance)
   - But mathematically, you double your chances of winning by switching doors!
   
   **The Math:**
   - If you don't switch, your chance of winning is 1/3 (33.3%)
   - If you do switch, your chance of winning is 2/3 (66.7%)
   
   This counterintuitive result has confused many people, including mathematicians!
   The key is that the host's action of revealing a goat gives you additional information.
   """)
# Add footer
st.markdown("---")
st.markdown("*Simulate the famous probability puzzle and see the results for yourself!*")