# src/utils.py

import os
import wave
import yt_dlp
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv
import openai

load_dotenv()

# ----------------------
# 🎵 Extract Audio
# ----------------------
def extract_audio_from_video(video_path, audio_path):
    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, codec='mp3')
        clip.close()
    except Exception as e:
        raise RuntimeError(f"Audio extraction failed: {e}")

# ----------------------
# 📝 Transcribe Audio
# ----------------------
def transcribe_audio(audio_path):
    client = openai.OpenAI()

    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text"
        )
    return transcript

# ----------------------
# 🧠 Summarize Transcript
# ----------------------
def create_summary(transcript_text):
    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Summarize the following transcript clearly and concisely."},
            {"role": "user", "content": transcript_text}
        ]
    )
    return response.choices[0].message.content.strip()

# ----------------------
# ❓ Create Quiz
# ----------------------
def create_quiz(summary_text):
    client = openai.OpenAI()

    prompt = f"""
    Create 5 multiple-choice questions from the following summary. 
    For each question, provide 4 options (labeled A, B, C, D), indicate the correct one, and give a short explanation.

    Summary:
    {summary_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful quiz generator."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = response.choices[0].message.content.strip()

    # Parse quiz using simple logic (assumes strict format)
    return parse_quiz(raw_text)

# ----------------------
# 🧠 Parse Quiz
# ----------------------
def parse_quiz(text):
    import re
    quizzes = []
    questions = text.split("\n\n")
    for q in questions:
        lines = q.strip().split("\n")
        if len(lines) < 6:
            continue
        question = lines[0].strip()
        options = {
            "A": lines[1].split("A.")[1].strip() if "A." in lines[1] else lines[1].strip(),
            "B": lines[2].split("B.")[1].strip() if "B." in lines[2] else lines[2].strip(),
            "C": lines[3].split("C.")[1].strip() if "C." in lines[3] else lines[3].strip(),
            "D": lines[4].split("D.")[1].strip() if "D." in lines[4] else lines[4].strip(),
        }
        correct = re.search(r"Correct Answer: ([ABCD])", q)
        explanation = re.search(r"Explanation: (.+)", q)
        quizzes.append({
            "question": question,
            "options": options,
            "correct_answer": correct.group(1) if correct else "A",
            "explanation": explanation.group(1) if explanation else ""
        })
    return quizzes
