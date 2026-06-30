import streamlit as st
import datetime
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="GATE WakeUp Challenge", page_icon="⏰", layout="wide")

# --- INITIALIZE TRACKING DATA ---
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'solved_count' not in st.session_state: st.session_state.solved_count = 0
if 'wrong_attempts' not in st.session_state: st.session_state.wrong_attempts = 0
if 'mistake_book' not in st.session_state: st.session_state.mistake_book = []
if 'alarm_cleared' not in st.session_state: st.session_state.alarm_cleared = False

# --- CSS FOR SIMULATING PHONE LOCKSCREEN ---
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #FFFFFF; }
    div.stButton > button:first-child { background-color: #FF4B4B; color: white; border-radius:12px; font-weight: bold; width: 100%; }
    .lock-box { background-color: #161A26; padding: 25px; border-radius: 18px; border: 2px solid #FF4B4B; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- DATES & TIMELINE LOGIC (FIXED FOR JUNE 30, 2026) ---
today = datetime.date(2026, 6, 30) 
start_date = datetime.date(2026, 7, 1) # Prep starts tomorrow!
exam_date = datetime.date(2027, 2, 7)  # Expected GATE 2027 weekend

days_left = (exam_date - today).days

# Dynamically calculate what day of prep you are on
if today < start_date:
    current_day_str = "Day 0 (Kickoff Tomorrow morning!)"
else:
    day_count = (today - start_date).days + 1
    current_day_str = f"Day {day_count} of 225"

# --- TOP GLOBAL STATS BAR ---
st.title("📳 GATE WakeUp Challenge")
st.caption(f"📅 Today's Date: June 30, 2026 | 🚀 Current Status: {current_day_str}")

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("🔥 Daily Streak", f"{st.session_state.streak} Days")
with c2: st.metric("🏆 Total XP Earned", f"{st.session_state.xp} XP")
with c3: st.metric("📚 Solved Count", f"{st.session_state.solved_count} PYQs")
with c4: st.metric("🎯 Exam Countdown", f"{days_left} Days")

st.markdown("---")

# --- NAVIGATION MENU ---
menu = st.radio("📱 App System Modules", ["⏰ Morning WakeUp Lock", "📝 My Mistake Book", "📊 Analytics Dashboard"], horizontal=True)

# ==========================================
# MODULE 1: MORNING WAKEUP CHALLENGE
# ==========================================
if menu == "⏰ Morning WakeUp Lock":
    st.subheader("🚨 Active System Wake-Lock Simulation")
    
    if today < start_date:
        st.info("🔒 System is locked in **Pre-Kickoff Mode** tonight. Your very first morning alarm puzzle will trigger tomorrow morning, July 1, 2026!")
        st.markdown("""
        <div class="lock-box" style="border-color: #4B9EFF;">
            <h4>🧠 Previewing Tomorrow's Day 1 Challenge Profile:</h4>
            <p>• <b>Subject Focus:</b> Operating Systems (Deadlocks) & Discrete Math (Sets)<br>
            • <b>Challenge Target:</b> 3 Correct responses required to silence alarm engine.<br>
            • <b>Rule Constraint:</b> Snooze button is disabled after 1 hit.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        if not st.session_state.alarm_cleared:
            st.error("🔒 PHONE SYSTEM IS LOCKED! You must correctly solve this GATE CSE problem to turn off the vibration engine.")
            
            st.markdown("""
            <div class="lock-box">
                <h4>🧠 Question 1 of 1 (Subject: Operating Systems)</h4>
                <p>A system has 4 processes sharing 3 instances of a resource type. Each process needs a maximum of 2 instances. Can a deadlock occur in this configuration?</p>
            </div>
            """, unsafe_allow_html=True)
            
            choice = st.radio("Select your absolute answer definition:", [
                "Yes, if all requests occur concurrently.",
                "No, deadlock is completely impossible here.",
                "Yes, depending on scheduling algorithms.",
                "Insufficient data to compute state space."
            ])
            
            if st.button("SUBMIT AND ATTEMPT DISMISSAL"):
                if choice == "No, deadlock is completely impossible here.":
                    st.session_state.alarm_cleared = True
                    st.session_state.solved_count += 1
                    st.session_state.xp += 100
                    st.session_state.streak = 1
                    st.balloons()
                    st.rerun()
                else:
                    st.sidebar.error("❌ Wrong Answer! Alarm remains active. Puzzle logged into Mistake Book.")
                    st.session_state.wrong_attempts += 1
                    if "OS Deadlock Configuration" not in st.session_state.mistake_book:
                        st.session_state.mistake_book.append("OS Deadlock Configuration")
        else:
            st.success("🎉 ALARM DISMISSED! Good morning! Your brain is awake. Go crush your preparation targets now!")
            if st.button("Reset Simulator for Tomorrow morning"):
                st.session_state.alarm_cleared = False
                st.rerun()

# ==========================================
# MODULE 2: MISTAKE BOOK
# ==========================================
elif menu == "📝 My Mistake Book":
    st.header("📖 Your Weakness Revision Log")
    st.caption("AI-managed targets using Spaced Repetition weights")
    
    if len(st.session_state.mistake_book) == 0:
        st.info("Your Mistake Book is completely clean. Fail puzzles during morning alarms to build your active study review lists!")
    else:
        for item in st.session_state.mistake_book:
            st.warning(f"⚠️ **Topic Pending Review:** {item}")
            st.write("👉 *AI Suggestion: Re-evaluate Core formulas for this topic before tonight's 11:30 PM cutoff.*")

# ==========================================
# MODULE 3: ANALYTICS DASHBOARD
# ==========================================
elif menu == "📊 Analytics Dashboard":
    st.header("📊 Performance Framework Overview")
    
    col_a, col_b = st.columns(2)
    with col_a:
        total_attempts = st.session_state.solved_count + st.session_state.wrong_attempts
        accuracy = (st.session_state.solved_count / total_attempts * 100) if total_attempts > 0 else 0.0
        st.metric("📊 WakeUp Accuracy Ratio", f"{accuracy:.1f}%")
    with col_b:
        st.metric("🔥 Total Failed Morning Snoozes", f"{st.session_state.wrong_attempts} Times")

    st.subheader("📅 Wakeup History Metrics")
    st.info("System is waiting for your morning alarm to sound. Sleep well tonight, and wake up ready to dominate Day 1! 🔥")
