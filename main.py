import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from gtts import gTTS
from datetime import datetime

app = FastAPI(
    title="AI Content Agent",
    version="0.1.0",
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}

@app.get("/")
async def root():
    return {
        "message": "مرحباً بك في AI Content Agent",
        "status": "تشغيل"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "سليم ✅",
        "service": "AI Content Agent"
    }

@app.post("/generate-scenario")
async def generate_scenario(topic: str, language: str = "ar"):
    try:
        prompt = f"""أنت متخصص في كتابة سيناريوهات الفيديو الاحترافية.
اكتب سيناريو قصير جداً (3-4 جمل فقط) باللغة {language} عن الموضوع التالي:
الموضوع: {topic}
يجب أن يكون السيناريو واضح وسهل الفهم وملائم للفيديو (مدة 3-5 دقائق) وجذاب ومثير للاهتمام.
السيناريو:"""
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        scenario_text = result[0]["generated_text"] if isinstance(result, list) and "generated_text" in result[0] else "لم يتم العثور على سيناريو"
        return {
            "topic": topic,
            "language": language,
            "scenario": scenario_text,
            "status": "نجح ✅"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "فشل ❌"
        }

@app.post("/text-to-speech")
async def text_to_speech(text: str, language: str = "ar"):
    try:
        if not os.path.exists("audio_files"):
            os.makedirs("audio_files")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"audio_files/audio_{timestamp}.mp3"

        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(audio_file)

        return {
            "text": text,
            "language": language,
            "audio_file": audio_file,
            "status": "نجح ✅"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "فشل ❌"
        }

@app.post("/generate-content")
async def generate_content(topic: str, language: str = "ar"):
    try:
        # خطوة 1: توليد السيناريو
        prompt = f"""أنت متخصص في كتابة سيناريوهات الفيديو الاحترافية.
اكتب سيناريو قصير جداً (3-4 جمل فقط) باللغة {language} عن الموضوع التالي:
الموضوع: {topic}
يجب أن يكون السيناريو واضح وسهل الفهم وملائم للفيديو (مدة 3-5 دقائق) وجذاب ومثير للاهتمام.
السيناريو:"""
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        scenario_text = result[0]["generated_text"] if isinstance(result, list) and "generated_text" in result[0] else "لم يتم العثور على سيناريو"

        # خطوة 2: تحويل السيناريو لصوت
        if not os.path.exists("audio_files"):
            os.makedirs("audio_files")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"audio_files/audio_{timestamp}.mp3"

        tts = gTTS(text=scenario_text, lang=language, slow=False)
        tts.save(audio_file)

        return {
            "topic": topic,
            "language": language,
            "scenario": scenario_text,
            "audio_file": audio_file,
            "status": "نجح ✅"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "فشل ❌"
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True
    )
