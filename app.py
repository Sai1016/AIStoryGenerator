import streamlit as st
from ai_engine import generate_story

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MyAvatar Story Generator",
    page_icon="📖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.sub-title {
    text-align: center;
    font-size: 1.05rem;
    color: #666;
    margin-bottom: 1.8rem;
}
.story-box {
    padding: 1rem 1.2rem;
    border-radius: 14px;
    background-color: #f8f9fa;
    border: 1px solid #e6e6e6;
    margin-bottom: 1rem;
}
.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
}
.choice-card {
    padding: 0.8rem 1rem;
    border: 1px solid #e6e6e6;
    border-radius: 12px;
    background: #ffffff;
    margin-bottom: 0.6rem;
}
.small-note {
    font-size: 0.9rem;
    color: #777;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">📚 MyAvatar Story Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Create an interactive story with guided choices and your own custom path.</div>',
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "started" not in st.session_state:
    st.session_state.started = False

if "story_ended" not in st.session_state:
    st.session_state.story_ended = False

if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0

if "hook" not in st.session_state:
    st.session_state.hook = ""

if "choices" not in st.session_state:
    st.session_state.choices = []

MAX_TURNS = 3


# ---------------- HELPERS ----------------
def extract_three_choices(text: str):
    """
    Extract up to exactly 3 visible choices from a response.
    Accepts lines starting with 1., 2., 3., -, •
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    found = []

    for line in lines:
        cleaned = line.strip()
        if (
            cleaned.startswith("1.")
            or cleaned.startswith("2.")
            or cleaned.startswith("3.")
            or cleaned.startswith("-")
            or cleaned.startswith("•")
        ):
            cleaned = cleaned.lstrip("1234567890.-• ").strip()
            if cleaned:
                found.append(cleaned)

    # keep only first 3
    return found[:3]


def has_story_end(text: str) -> bool:
    upper = text.upper()
    return "THE END" in upper or "STORY_END" in upper


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("Settings")

    genre = st.selectbox(
        "Select Genre",
        ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Comedy"]
    )

    temp = st.slider(
        "Creativity temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    st.markdown("---")

    if st.button("Reset Story", use_container_width=True):
        st.session_state.history = []
        st.session_state.started = False
        st.session_state.story_ended = False
        st.session_state.turn_count = 0
        st.session_state.hook = ""
        st.session_state.choices = []
        st.rerun()

# ---------------- MAIN LAYOUT ----------------
left_col, right_col = st.columns([1, 1.45], gap="large")

# ---------------- LEFT PANEL ----------------
with left_col:
    st.markdown('<div class="section-title">Start Your Story</div>', unsafe_allow_html=True)

    if not st.session_state.started:
        hook = st.text_area(
            "Initial Hook / Setting",
            placeholder="Example: A young mage finds a locked door beneath an ancient ruined city...",
            height=180
        )

        if st.button("Start Story", use_container_width=True):
            if not hook.strip():
                st.warning("Please enter an initial hook to begin the story.")
            else:
                st.session_state.hook = hook.strip()

                first_part = generate_story(
                    history=[],
                    genre=genre,
                    prompt_type="start",
                    user_input=st.session_state.hook,
                    temp=temp
                )

                st.session_state.history.append({"role": "assistant", "text": first_part})
                st.session_state.started = True
                st.session_state.turn_count = 1
                st.session_state.choices = []

                if has_story_end(first_part):
                    st.session_state.story_ended = True

                st.rerun()

    else:
        st.markdown('<div class="section-title">Continue the Story</div>', unsafe_allow_html=True)

        if st.session_state.story_ended:
            st.success("This story has reached its ending.")
        else:
            user_text = st.text_input(
                "Add your own next step",
                placeholder="Example: The hero quietly takes the glowing key."
            )

            # ---------- Button Row 1 ----------
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Continue with AI", use_container_width=True):
                    if user_text.strip():
                        st.session_state.history.append({"role": "user", "text": user_text.strip()})

                    mode = "end" if st.session_state.turn_count >= MAX_TURNS - 1 else "continue"

                    ai_response = generate_story(
                        history=st.session_state.history,
                        genre=genre,
                        prompt_type=mode,
                        temp=temp
                    )

                    st.session_state.history.append({"role": "assistant", "text": ai_response})
                    st.session_state.turn_count += 1
                    st.session_state.choices = []

                    if st.session_state.turn_count >= MAX_TURNS or has_story_end(ai_response):
                        st.session_state.story_ended = True

                    st.rerun()

            with col2:
                if st.button("Get 3 Choices", use_container_width=True):
                    if user_text.strip():
                        st.session_state.history.append({"role": "user", "text": user_text.strip()})

                    mode = "end" if st.session_state.turn_count >= MAX_TURNS - 1 else "choices"

                    choices_response = generate_story(
                        history=st.session_state.history,
                        genre=genre,
                        prompt_type=mode,
                        temp=temp
                    )

                    st.session_state.history.append({"role": "assistant", "text": choices_response})
                    st.session_state.turn_count += 1

                    # extract only 3 choices for button display
                    st.session_state.choices = extract_three_choices(choices_response)

                    if st.session_state.turn_count >= MAX_TURNS or has_story_end(choices_response):
                        st.session_state.story_ended = True

                    st.rerun()

            # ---------- Button Row 2 ----------
            st.markdown("#### Choose a suggested option")
            if st.session_state.choices:
                for idx, choice in enumerate(st.session_state.choices, start=1):
                    st.markdown(
                        f'<div class="choice-card"><b>Option {idx}:</b> {choice}</div>',
                        unsafe_allow_html=True
                    )
                    if st.button(f"Use Option {idx}", key=f"use_option_{idx}", use_container_width=True):
                        st.session_state.history.append({"role": "user", "text": choice})

                        mode = "end" if st.session_state.turn_count >= MAX_TURNS - 1 else "continue"

                        ai_response = generate_story(
                            history=st.session_state.history,
                            genre=genre,
                            prompt_type=mode,
                            temp=temp
                        )

                        st.session_state.history.append({"role": "assistant", "text": ai_response})
                        st.session_state.turn_count += 1
                        st.session_state.choices = []

                        if st.session_state.turn_count >= MAX_TURNS or has_story_end(ai_response):
                            st.session_state.story_ended = True

                        st.rerun()
            else:
                st.markdown('<div class="small-note">Click "Get 3 Choices" to generate three guided options.</div>', unsafe_allow_html=True)

            st.markdown("#### Or create your own option")
            if st.button("Add Your Option", use_container_width=True):
                if not user_text.strip():
                    st.warning("Please type your custom option first.")
                else:
                    st.session_state.history.append({"role": "user", "text": user_text.strip()})

                    mode = "end" if st.session_state.turn_count >= MAX_TURNS - 1 else "continue"

                    ai_response = generate_story(
                        history=st.session_state.history,
                        genre=genre,
                        prompt_type=mode,
                        temp=temp
                    )

                    st.session_state.history.append({"role": "assistant", "text": ai_response})
                    st.session_state.turn_count += 1
                    st.session_state.choices = []

                    if st.session_state.turn_count >= MAX_TURNS or has_story_end(ai_response):
                        st.session_state.story_ended = True

                    st.rerun()

            st.caption(f"Story progress: Turn {st.session_state.turn_count} / {MAX_TURNS}")

# ---------------- RIGHT PANEL ----------------
with right_col:
    st.markdown('<div class="section-title">Your Story</div>', unsafe_allow_html=True)

    if not st.session_state.started:
        st.info("Your story will appear here once you click **Start Story**.")
    else:
        for msg in st.session_state.history:
            role = msg["role"]
            text = msg["text"]

            if role == "user":
                with st.chat_message("user"):
                    st.write(text)
            else:
                with st.chat_message("assistant"):
                    st.markdown(f'<div class="story-box">{text}</div>', unsafe_allow_html=True)

        if st.session_state.story_ended:
            st.success("✨ The story has ended.")