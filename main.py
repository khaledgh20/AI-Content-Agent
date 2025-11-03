import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ollama
from gtts import gTTS
import os
from datetime import datetime

app = FastAPI(
    title="AI Content Agent",
    version="0.1.0",
    debug=True,
)

# CORS middleware
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ollama
from gtts import gTTS
import os
from datetime import datetime

app = FastAPI(
    title="AI Content Agent",
    version="0.1.0",
    debug=True,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000", "http://localhost:8000", "file://"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    """
    توليد سيناريو للفيديو باستخدام Ollama
    
    مثال:
    /generate-scenario?topic=تعليم%20البرمجة&language=ar
    """
    try:
        prompt = f"""
أنت متخصص في كتابة سيناريوهات الفيديو الاحترافية.
اكتب سيناريو قصير جداً (3-4 جمل فقط) باللغة {language} عن الموضوع التالي:
الموضوع: {topic}

يجب أن يكون السيناريو:
- واضح وسهل الفهم
- ملائم للفيديو (مدة 3-5 دقائق)
- جذاب ومثير للاهتمام

السيناريو:
        """
        
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            stream=False,
        )
        
        scenario_text = response['response']
        
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
    """
    تحويل النص إلى صوت باستخدام Google TTS
    
    مثال:
    /text-to-speech?text=مرحبا%20بك&language=ar
    """
    try:
        # إنشاء مجلد للملفات الصوتية
        if not os.path.exists("audio_files"):
            os.makedirs("audio_files")
        
        # اسم الملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"audio_files/audio_{timestamp}.mp3"
        
        # تحويل النص لصوت
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
    """
    توليد محتوى كامل (سيناريو + صوت) بضغطة زر واحدة!
    
    مثال:
    /generate-content?topic=تعليم%20البرمجة&language=ar
    """
    try:
        # خطوة 1: توليد السيناريو من Ollama
        prompt = f"""
أنت متخصص في كتابة سيناريوهات الفيديو الاحترافية.
اكتب سيناريو قصير جداً (3-4 جمل فقط) باللغة {language} عن الموضوع التالي:
الموضوع: {topic}

يجب أن يكون السيناريو:
- واضح وسهل الفهم
- ملائم للفيديو (مدة 3-5 دقائق)
- جذاب ومثير للاهتمام

السيناريو:
        """
        
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            stream=False,
        )
        
        scenario_text = response['response']
        
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
        host="127.0.0.1",
        port=8000,
        reload=True
    )
## **الطريقة:**

**1. اضغط على السطر 18** (الخط `allow_origins=["*"],`)

**2. اختر كل النص:**
```
Ctrl + A
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    """
    توليد سيناريو للفيديو باستخدام Ollama
    
    مثال:
    /generate-scenario?topic=تعليم%20البرمجة&language=ar
    """
    try:
        prompt = f"""
أنت متخصص في كتابة سيناريوهات الفيديو الاحترافية.
اكتب سيناريو قصير جداً (3-4 جمل فقط) باللغة {language} عن الموضوع التالي:
الموضوع: {topic}

يجب أن يكون السيناريو:
- واضح وسهل الفهم
- ملائم للفيديو (مدة 3-5 دقائق)
- جذاب ومثير للاهتمام

السيناريو:
        """
        
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            stream=False,
        )
        
        scenario_text = response['response']
        
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
    """
    تحويل النص إلى صوت باستخدام Google TTS
    
    مثال:
    /text-to-speech?text=مرحبا%20بك&language=ar
    """
    try:
        # إنشاء مجلد للملفات الصوتية
        if not os.path.exists("audio_files"):
            os.makedirs("audio_files")
        
        # اسم الملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"audio_files/audio_{timestamp}.mp3"
        
        # تحويل النص لصوت
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
    """
    توليد محتوى كامل (سيناريو + صوت) بضغطة زر واحدة!
    
    مثال:
    /generate-content?topic=تعليم%20البرمجة&language=ar
    """
    try:
        # خطوة 1: توليد السيناريو من Ollama
        prompt = f"""
أنت متخصص في كتابة سيناريوهات الفيديو الاحترافية.
اكتب سيناريو قصير جداً (3-4 جمل فقط) باللغة {language} عن الموضوع التالي:
الموضوع: {topic}

يجب أن يكون السيناريو:
- واضح وسهل الفهم
- ملائم للفيديو (مدة 3-5 دقائق)
- جذاب ومثير للاهتمام

السيناريو:
        """
        
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            stream=False,
        )
        
        scenario_text = response['response']
        
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
        host="127.0.0.1",
        port=8000,
        reload=True
    )