import streamlit as st
import tempfile
from gemini_client import GeminiClient

st.set_page_config(
    page_title="Gemini Finance Analyzer",
    page_icon="📊",
    layout="wide",
)

# --- Header ---
st.markdown(
    """
    <style>
    .big-title {
        font-size: 2.8rem !important;
        text-align: center;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2em;
    }
    .subtitle {
        text-align: center;
        color: #f0f4f8;
        font-size: 1.2rem;
        margin-bottom: 2em;
    }
    .stButton>button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6em 1.2em !important;
        font-weight: 600 !important;
    }
    </style>
    <p class="big-title">📊 Gemini Finance Analyzer</p>
    <p class="subtitle">Upload financial or healthcare documents and get AI-powered insights in seconds.</p>
    """,
    unsafe_allow_html=True,
)

# --- File uploader ---
uploaded_file = st.file_uploader(
    "📁 Upload your file (PDF, CSV, Excel, or TXT)",
    type=["pdf", "csv", "xlsx", "txt"],
)

if uploaded_file:
    # Save uploaded file to temp path
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    st.info("⏳ Analyzing your file with Gemini... please wait.", icon="🔍")
    client = GeminiClient()
    result = client.analyze_file(temp_path)

    st.success("✅ Analysis complete!")
    st.markdown("---")

    # --- Clean & parse output ---
    lines = [line.strip() for line in result.split("\n") if line.strip()]

    # Remove any text before first section header
    first_header_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("### 📘 Overview"):
            first_header_idx = i
            break
    lines = lines[first_header_idx:]  # discard everything before the first header

    # --- Organize by section ---
    sections = {
        "📘 Overview": [],
        "💰 Financial Insights": [],
        "🩺 Healthcare / Other Insights": [],
        "🧭 Key Takeaways": [],
    }

    current_section = None
    for line in lines:
        if line.startswith("### 📘 Overview"):
            current_section = "📘 Overview"
            continue
        elif line.startswith("### 💰 Financial Insights"):
            current_section = "💰 Financial Insights"
            continue
        elif line.startswith("### 🩺 Healthcare/Other Insights") or line.startswith("### 🩺 Healthcare / Other Insights"):
            current_section = "🩺 Healthcare / Other Insights"
            continue
        elif line.startswith("### 🧭 Key Takeaways"):
            current_section = "🧭 Key Takeaways"
            continue

        if current_section:
            sections[current_section].append(line)

    # --- Dashboard layout ---
    col1, col2 = st.columns(2)

    # Left column
    with col1:
        if sections["📘 Overview"]:
            st.subheader("📘 Overview")
            st.markdown(
                "<div style='background-color:#1c3a91; padding:15px; border-radius:10px; color:#fff;'>"
                + "<br>".join(sections["📘 Overview"])
                + "</div>",
                unsafe_allow_html=True,
            )

        if sections["💰 Financial Insights"]:
            st.subheader("💰 Financial Insights")
            st.markdown(
                "<div style='background-color:#0b6623; padding:15px; border-radius:10px; color:#fff;'>"
                + "<br>".join(sections["💰 Financial Insights"])
                + "</div>",
                unsafe_allow_html=True,
            )

    # Right column
    with col2:
        if sections["🩺 Healthcare / Other Insights"]:
            st.subheader("🩺 Healthcare / Other Insights")
            st.markdown(
                "<div style='background-color:#b86b00; padding:15px; border-radius:10px; color:#fff;'>"
                + "<br>".join(sections["🩺 Healthcare / Other Insights"])
                + "</div>",
                unsafe_allow_html=True,
            )

        if sections["🧭 Key Takeaways"]:
            st.subheader("🧭 Key Takeaways")
            st.markdown(
                "<div style='background-color:#8b0000; padding:15px; border-radius:10px; color:#fff;'>"
                + "<br>".join(sections["🧭 Key Takeaways"])
                + "</div>",
                unsafe_allow_html=True,
            )

   
else:
    st.info("👆 Upload a file to begin.")
