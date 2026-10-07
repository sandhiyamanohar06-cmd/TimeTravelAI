import os
import re
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="TimeShift AI",
    page_icon="🌀",
    layout="wide"
)

# ================= DESIGN =================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 50% 0%, #172554 0%, transparent 35%),
        #020617;
    color: white;
}

.block-container {
    max-width: 1050px;
    padding-top: 55px;
}

/* HEADER */

.title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.title span {
    color: #60a5fa;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 17px;
    margin-bottom: 45px;
}

/* INPUT */

label {
    color: #dbeafe !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

textarea {
    background: #0f172a !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    font-size: 16px !important;
}

div.stButton > button {
    width: 100%;
    height: 56px;
    border-radius: 30px;
    border: none;
    background: linear-gradient(90deg, #0ea5e9, #7c3aed);
    color: white;
    font-size: 17px;
    font-weight: 700;
    margin-top: 12px;
}

.portal {
    text-align: center;
    color: #60a5fa;
    font-size: 13px;
    letter-spacing: 3px;
    margin-top: 25px;
}

/* OUTPUT HEADER */

.output-title {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: #bfdbfe;
    margin-top: 55px;
    margin-bottom: 25px;
}

.output-line {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #2563eb,
        #7c3aed,
        transparent
    );
    margin-bottom: 25px;
}

/* SECTION */

.section {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid #1e3a8a;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 18px;
}

.section-title {
    color: #7dd3fc;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}

.section-text {
    color: #dbeafe;
    line-height: 1.7;
    font-size: 15px;
}

/* TWO COLUMN CARDS */

.card-row {
    display: flex;
    gap: 18px;
    margin-bottom: 18px;
}

.small-card {
    flex: 1;
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid #1e3a8a;
    border-radius: 16px;
    padding: 22px;
}

.small-title {
    color: #93c5fd;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* SCORE */

.score-box {
    text-align: center;
    background: linear-gradient(
        135deg,
        rgba(14, 165, 233, 0.12),
        rgba(124, 58, 237, 0.12)
    );
    border: 1px solid #7c3aed;
    border-radius: 18px;
    padding: 25px;
    margin-top: 18px;
}

.score-number {
    font-size: 42px;
    font-weight: 800;
    color: #a5b4fc;
}

.score-label {
    color: #94a3b8;
    font-size: 13px;
    letter-spacing: 2px;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #475569;
    font-size: 13px;
    margin-top: 45px;
}

</style>
""", unsafe_allow_html=True)


# ================= HEADER =================

st.markdown(
    '<div class="title">🌀 TIME<span>SHIFT</span> AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Change one moment in history. Discover a different future.'
    '</div>',
    unsafe_allow_html=True
)


# ================= INPUT =================

event = st.text_area(
    "What if...?",
    placeholder="Example: What if the Internet was invented in 1950?",
    height=150
)

simulate = st.button(
    "🚀 INITIATE TIME TRAVEL",
    use_container_width=True
)

st.markdown(
    '<div class="portal">◈ TIME PORTAL READY ◈</div>',
    unsafe_allow_html=True
)


# ================= AI =================

if simulate:

    if not event.strip():

        st.warning("Please enter a historical event.")

    elif not api_key:

        st.error("API key not found. Please check your .env file.")

    else:

        with st.spinner("🌀 Calculating alternate timeline..."):

            try:

                client = OpenAI(api_key=api_key)

                prompt = f"""
You are TimeShift AI, an alternate-history simulator.

Historical event:
{event}

Create a SHORT fictional alternate timeline.

RULES:
- Use very simple English.
- No difficult words.
- Maximum 5 important years.
- Each year must have one short sentence.
- Keep every section short.
- Exactly 2 bullets for Technology.
- Exactly 2 bullets for Economy.
- Exactly 2 bullets for Society.
- Exactly 2 bullets for Paradox.
- Give a score from 0 to 100.

Use EXACTLY this format:

KEY YEARS
1950 — ...
1960 — ...
1970 — ...
1980 — ...
1990 — ...

TECHNOLOGY
• ...
• ...

ECONOMY
• ...
• ...

SOCIETY
• ...
• ...

PARADOX
• ...
• ...

SCORE
XX/100

REASON
One short sentence.

This is fictional AI-generated content, not a real prediction.
"""

                response = client.responses.create(
                    model="gpt-6-luna",
                    input=prompt
                )

                output = response.output_text

                # ================= OUTPUT HEADER =================

                st.markdown(
                    '<div class="output-title">🌌 ALTERNATE UNIVERSE</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="output-line"></div>',
                    unsafe_allow_html=True
                )

                # ================= PARSE OUTPUT =================

                def get_section(name, next_names):
                    pattern = rf"{name}\s*(.*?)(?=\n(?:{'|'.join(next_names)})\s*|\Z)"
                    match = re.search(
                        pattern,
                        output,
                        re.IGNORECASE | re.DOTALL
                    )
                    return match.group(1).strip() if match else ""

                key_years = get_section(
                    "KEY YEARS",
                    ["TECHNOLOGY", "ECONOMY", "SOCIETY", "PARADOX", "SCORE"]
                )

                technology = get_section(
                    "TECHNOLOGY",
                    ["ECONOMY", "SOCIETY", "PARADOX", "SCORE"]
                )

                economy = get_section(
                    "ECONOMY",
                    ["SOCIETY", "PARADOX", "SCORE"]
                )

                society = get_section(
                    "SOCIETY",
                    ["PARADOX", "SCORE"]
                )

                paradox = get_section(
                    "PARADOX",
                    ["SCORE"]
                )

                score_match = re.search(
                    r"SCORE\s*(\d{1,3})\s*/\s*100",
                    output,
                    re.IGNORECASE
                )

                score = score_match.group(1) if score_match else "—"

                reason_match = re.search(
                    r"REASON\s*(.*)",
                    output,
                    re.IGNORECASE | re.DOTALL
                )

                reason = (
                    reason_match.group(1).strip()
                    if reason_match
                    else ""
                )

                # ================= KEY YEARS =================

                if key_years:
                    st.markdown(
                        '<div class="section">'
                        '<div class="section-title">📅 KEY YEARS</div>'
                        f'<div class="section-text">{key_years.replace(chr(10), "<br>")}</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                # ================= TECHNOLOGY + ECONOMY =================

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        '<div class="small-card">'
                        '<div class="small-title">💻 TECHNOLOGY</div>'
                        f'<div class="section-text">{technology.replace(chr(10), "<br>")}</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        '<div class="small-card">'
                        '<div class="small-title">💰 ECONOMY</div>'
                        f'<div class="section-text">{economy.replace(chr(10), "<br>")}</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                # ================= SOCIETY =================

                if society:
                    st.markdown(
                        '<div class="section">'
                        '<div class="section-title">👥 SOCIETY</div>'
                        f'<div class="section-text">{society.replace(chr(10), "<br>")}</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                # ================= PARADOX =================

                if paradox:
                    st.markdown(
                        '<div class="section">'
                        '<div class="section-title">⚠️ PARADOX</div>'
                        f'<div class="section-text">{paradox.replace(chr(10), "<br>")}</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                # ================= SCORE =================

                st.markdown(
                    '<div class="score-box">'
                    '<div class="score-label">🧩 PARADOX SCORE</div>'
                    f'<div class="score-number">{score}<span style="font-size:20px;">/100</span></div>'
                    f'<div class="section-text">{reason}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.success("🌀 Timeline simulation completed!")

            except Exception as e:

                st.error("Something went wrong.")
                st.code(str(e))


# ================= FOOTER =================

st.markdown(
    '<div class="footer">'
    'TimeShift AI • Powered by Artificial Intelligence'
    '</div>',
    unsafe_allow_html=True
)