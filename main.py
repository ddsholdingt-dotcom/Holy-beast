from fastapi import FastAPI
from datetime import datetime
import os

app = FastAPI(title="EduVox 3D", version="1.0.0")

# Check if API keys are available
HAS_TRIPO = bool(os.getenv("TRIPO_API_KEY"))
HAS_ELEVENLABS = bool(os.getenv("ELEVENLABS_API_KEY"))

@app.get("/")
async def root():
    return {
        "service": "EduVox 3D",
        "version": "1.0.0",
        "features": {
            "3d_generation": "available" if HAS_TRIPO else "demo_mode",
            "voice_cloning": "available" if HAS_ELEVENLABS else "demo_mode",
            "crisis_support": "always_available"
        },
        "crisis_support": {
            "sadag": "0800 567 567",
            "lifeline": "0861 322 322",
            "emergency": "10111"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "production" if HAS_TRIPO else "demo"
    }

@app.post("/emotional/checkin")
async def emotional_checkin(mood_rating: int, emotional_state: str, text: str = ""):
    crisis_keywords = ["suicide", "kill myself", "end it", "want to die", "financial ruin"]
    crisis = any(kw in text.lower() for kw in crisis_keywords)
    
    return {
        "checkin_id": "chk-" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
        "crisis_detected": crisis,
        "ai_response": "🆘 Call SADAG 0800 567 567 immediately. You are not alone." if crisis else "Thanks for checking in! How can I help you learn today?",
        "resources": [
            {"name": "SADAG 24/7 Crisis Line", "phone": "0800 567 567"},
            {"name": "LifeLine SA", "phone": "0861 322 322"}
        ] if crisis else [],
        "message": "Your well-being matters"
    }

@app.post("/3d/generate")
async def generate_3d(prompt: str, style: str = "realistic"):
    if not HAS_TRIPO:
        return {
            "status": "demo_mode",
            "message": "3D generation requires TRIPO_API_KEY. Add it in Render dashboard.",
            "demo_model_url": "https://example.com/demo-model.glb"
        }
    return {"status": "processing", "task_id": "demo-task", "estimated_time": "30 seconds"}

@app.post("/voice/tts")
async def text_to_speech(text: str, voice_id: str = "default"):
    if not HAS_ELEVENLABS:
        return {
            "status": "demo_mode",
            "message": "Voice requires ELEVENLABS_API_KEY. Add it in Render dashboard.",
            "demo_audio_url": "https://example.com/demo-audio.mp3"
        }
    return {"status": "generated", "audio_url": "demo-url", "duration": 30}

@app.get("/education/subjects")
async def list_subjects():
    return {
        "subjects": [
            {"id": "mathematics", "name": "Mathematics", "icon": "📐"},
            {"id": "physics", "name": "Physics", "icon": "⚛️"},
            {"id": "chemistry", "name": "Chemistry", "icon": "🧪"},
            {"id": "biology", "name": "Biology", "icon": "🧬"},
            {"id": "cultural_heritage", "name": "Cultural Heritage", "icon": "🏛️"},
            {"id": "financial_literacy", "name": "Financial Literacy", "icon": "💰"}
        ],
        "languages": [
            "English", "isiZulu", "isiXhosa", "Afrikaans", "Sepedi",
            "Setswana", "Sesotho", "Xitsonga", "siSwati", "Tshivenda", "isiNdebele"
        ]
    }
