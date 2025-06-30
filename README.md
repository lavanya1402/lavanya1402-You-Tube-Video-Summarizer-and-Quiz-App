# 🤖 YouTube Video Summarizer & Quiz Generator

An AI-powered application that combines **automated transcription, summarization, and quiz generation** using YouTube videos as input. Ideal for building **edtech tools**, **learning automation**, or **AI-driven knowledge checks**.

---

## 🚀 What This App Does

From an AI developer’s perspective:

* 🔗 **Ingests video content** via YouTube URL or upload
* 🗣️ **Transcribes** speech using OpenAI's `whisper-1` ASR model
* 🧠 **Summarizes** content via `gpt-4o` using LangChain pipelines
* 📋 **Generates multiple-choice questions** using structured output parsing with `Pydantic` + `LangChain`
* 🖥️ Built with `Streamlit` for lightweight UI
* 📦 Modularized code for integration into larger LLMOps pipelines

---

## 🧰 Tech Stack

| Layer        | Tool/Library    | Purpose                            |
| ------------ | --------------- | ---------------------------------- |
| LLM Backbone | OpenAI GPT-4o   | Summarization & Quiz Generation    |
| ASR          | OpenAI Whisper  | Transcription                      |
| UI           | Streamlit       | Lightweight frontend               |
| Workflow     | LangChain       | Prompt templating & chaining       |
| Video        | yt-dlp, MoviePy | Download + audio extraction        |
| Audio        | Pydub           | Format handling & chunking         |
| Parsing      | Pydantic + JSON | Quiz structure & output formatting |

---

## 📂 Folder Structure

```
video_summarise_quiz/
├── app.py                  # Flask backend (if used)
├── streamlit_app.py        # Main UI
├── yt_download.py          # YouTube ingestion
├── requirements.txt
├── src/
│   └── utils.py            # Transcription, parsing, helpers
├── uploads/                # Downloaded/transcoded files
└── README.md
```

---

## 🧪 Use Cases for AI Developers

* 🚀 **Fine-tuning pipelines** for edtech startups
* 🧠 **Knowledge distillation** from long-form media
* 🛠️ Build as a **microservice** in larger AI LLMOps platform
* 🧪 Test bed for **multi-modal learning pipelines**

---

## ⚡ Sample Prompt Engineering (LangChain)

```python
PromptTemplate(
    template="""
    Based on this summary:
    {summary}
    
    Generate a quiz in the following JSON format:
    {format_instructions}
    """,
    input_variables=["summary"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

---

## 🧠 Final Thought

This project showcases how **LLMs + ASR + lightweight UI** can work together to **unlock knowledge** from passive video content. Perfect for **building MVPs**, **showcasing AI capabilities**, or integrating into internal tools.

> “I tested this on a Krish Naik video… and failed the quiz myself. Back to learning!” 😅


