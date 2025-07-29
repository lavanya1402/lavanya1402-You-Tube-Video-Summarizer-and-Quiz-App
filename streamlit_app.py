import streamlit as st
import os
from src.utils import extract_audio_from_video, transcribe_audio, create_summary, create_quiz
from yt_download import download_youtube_video

# App title
st.title("🎥 Video Summarizer and Quiz App")

# Session state init
for key in ['video', 'transcript', 'summary', 'quizzes', 'quiz_yourself']:
    if key not in st.session_state:
        st.session_state[key] = None

# Temporary folders
temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)

# -------------------------
# 📁 Upload Video
# -------------------------
st.subheader("📤 Upload a Video File")
video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

if video_file:
    video_path = os.path.join(temp_dir, video_file.name)
    with open(video_path, "wb") as f:
        f.write(video_file.getbuffer())
    st.session_state.video = video_path
    st.video(video_path)

# -------------------------------
# 🌐 YouTube URL Download
# -------------------------------
st.subheader("🌐 Or Paste a YouTube Video URL")
youtube_url = st.text_input("Enter YouTube video URL")

if st.button("Download from YouTube"):
    if youtube_url.strip():
        with st.spinner("📥 Downloading..."):
            try:
                downloaded_path = download_youtube_video(youtube_url.strip(), output_dir=temp_dir)
                if downloaded_path:
                    st.session_state.video = downloaded_path
                    st.video(downloaded_path)
                    st.success("✅ Downloaded successfully!")
                else:
                    st.error("❌ Failed to download the video.")
            except Exception as e:
                st.error(f"❌ Download failed: {e}")
    else:
        st.warning("⚠️ Please enter a valid YouTube URL.")

# -----------------------------
# 🧠 Generate Transcript
# -----------------------------
if st.session_state.video and st.session_state.transcript is None:
    st.subheader("🎙️ Transcribing Audio...")
    with st.spinner("🔊 Extracting audio and calling Whisper..."):
        try:
            audio_path = os.path.join(temp_dir, "audio.mp3")
            extract_audio_from_video(st.session_state.video, audio_path)
            st.success("🎧 Audio extracted.")

            transcript = transcribe_audio(audio_path)
            if transcript.strip():
                st.session_state.transcript = transcript
                st.success("📝 Transcript ready!")
                st.subheader("🧾 Transcript Preview")
                st.code(transcript[:1000])  # Show first 1000 characters
            else:
                st.error("❌ No transcript returned from Whisper.")
        except Exception as e:
            st.error(f"❌ Transcription failed: {e}")

# -------------------------
# 📝 Generate Summary
# -------------------------
if st.button("Summarize"):
    if st.session_state.transcript:
        with st.spinner("🧠 Summarizing..."):
            st.session_state.summary = create_summary(st.session_state.transcript)
        st.subheader("📄 Summary")
        st.write(st.session_state.summary)
    else:
        st.warning("⚠️ Transcript not available yet.")

# -------------------------
# ❓ Generate Quiz
# -------------------------
if st.button("Quiz Yourself"):
    if not st.session_state.transcript:
        st.warning("⚠️ Transcript not available.")
    else:
        if st.session_state.summary is None:
            st.session_state.summary = create_summary(st.session_state.transcript)
        try:
            with st.spinner("🧠 Generating quiz..."):
                quizzes = create_quiz(st.session_state.summary)
                st.session_state.quizzes = quizzes
                st.session_state.quiz_yourself = True
        except Exception as e:
            st.error(f"❌ Error creating quiz: {e}")

# -------------------------
# ✅ Display Quiz
# -------------------------
def display_quiz():
    quiz_data = st.session_state.get("quizzes", [])
    if not quiz_data:
        st.error("❌ No quiz data available.")
        return

    if 'user_answers' not in st.session_state or len(st.session_state.user_answers) != len(quiz_data):
        st.session_state.user_answers = {idx: None for idx in range(len(quiz_data))}

    with st.form("quiz_form"):
        for idx, q in enumerate(quiz_data):
            st.write(f"**Q{idx+1}: {q['question']}**")
            options = list(q['options'].values())
            selected = st.selectbox(f"Select an answer:", [""] + options, key=f"select_{idx}")
            st.session_state.user_answers[idx] = selected if selected else None

        if st.form_submit_button("Submit"):
            for idx, q in enumerate(quiz_data):
                user_ans = st.session_state.user_answers.get(idx)
                correct = q['options'][q['correct_answer']]
                if user_ans == correct:
                    st.success(f"Q{idx+1}: ✅ Correct!")
                else:
                    st.error(f"Q{idx+1}: ❌ Incorrect. Correct: {correct}")
                if "explanation" in q:
                    st.info(f"Explanation: {q['explanation']}")

if st.session_state.quiz_yourself:
    display_quiz()
