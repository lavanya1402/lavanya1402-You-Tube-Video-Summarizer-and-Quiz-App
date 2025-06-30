import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field  # ✅ Corrected: use langchain_core.pydantic_v1
from openai import OpenAI

# ✅ Initialize OpenAI client for Whisper
client = OpenAI()

# ✅ Initialize LangChain LLM (GPT-4o)
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")


# ---------------------------
# 🎵 Extract Audio from Video
# ---------------------------
def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path, verbose=False, logger=None)
    audio.close()


# ------------------------------
# 🔊 Transcribe using Whisper API
# ------------------------------
def transcribe_audio_chunk(chunk_path):
    with open(chunk_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text


def transcribe_audio(audio_path):
    max_size = 24 * 1024 * 1024  # 24MB Whisper upload limit
    chunk_duration = 10 * 60 * 1000  # 10 minutes in ms
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)

    if os.path.getsize(audio_path) > max_size:
        transcript = ""
        for i in range(0, duration_ms, chunk_duration):
            chunk = audio[i:i + chunk_duration]
            chunk_path = f"{audio_path[:-4]}_chunk{i//1000}.mp3"
            chunk.export(chunk_path, format="mp3")
            transcript += transcribe_audio_chunk(chunk_path) + " "
            os.remove(chunk_path)
        return transcript.strip()
    else:
        return transcribe_audio_chunk(audio_path)


# -----------------------------
# 🧠 Quiz Schema + JSON Parser
# -----------------------------
class QuizQuestion(BaseModel):
    question: str = Field(description="The quiz question.")
    options: dict = Field(description="Answer options.")
    correct_answer: str = Field(description="Correct answer key.")
    explanation: str = Field(description="Explanation.")

parser = JsonOutputParser(pydantic_object=QuizQuestion)


# -----------------------------
# 📝 Summary Generator
# -----------------------------
def create_summary(transcript):
    template = """
    You are a helpful assistant. Summarize the content and extract key ideas.

    Transcript:
    {transcript}
    """
    prompt = PromptTemplate(template=template, input_variables=["transcript"])
    chain = prompt | llm
    return chain.invoke({"transcript": transcript}).content


# -----------------------------
# ❓ Quiz Generator
# -----------------------------
def create_quiz(summary):
    prompt = PromptTemplate(
        template=(
            "You are a quiz generator. Based on:\n{summary}\n"
            "Generate 10 multiple choice questions in JSON format:\n{format_instructions}"
        ),
        input_variables=["summary"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm | parser
    return chain.invoke({"summary": summary})
