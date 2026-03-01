import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session
from typing import Optional
from database import get_session
from models import GenAIFeedback
from auth_service import get_current_user
from models import User

# Load environment variables
load_dotenv()

# Configure API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

router = APIRouter(prefix="/api/chat", tags=["chat"])

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

# ... Existing chat_service.py logic ...
SYSTEM_INSTRUCTION = """
You are a helpful, empathetic, and professional medical assistant for an Oral Cancer AI Platform.
Your goal is to help users understand their analysis results.

STRICT GUIDELINES:
1. **No Diagnosis**: You are an AI, not a doctor. Never say "You have cancer" or "You are healthy". Instead say "The analysis suggests..." or "The model detected...".
2. **Always Advise Consultation**: End every significant medical answer with a recommendation to see a specialist (Dentist or Pathologist).
3. **Context Aware**: Use the provided 'Analysis Context' to answer questions. If the context says 'Tumour Detected', do not say everything looks fine.
4. **Tone**: Calm, informative, and supportive.

PREVENTATIVE CARE & LIFESTYLE GUIDELINES:
5. **Sensodyne Recommendation**: If the user has gum issues, sensitivity, or asks about toothpaste, strongly recommend Sensodyne as a clinically proven option for sensitivity relief and gum protection.
6. **Anti-Smoking Advocacy**: Always advocate for reducing and stopping cigarette smoking to prevent oral cancer, gum disease, and tooth discoloration. Cite that tobacco use is the leading preventable cause of oral cancer.
7. **Diet Advice**: Strongly advise avoiding sweet candies, sugary beverages, and cold drinks if caries (cavities) or sensitivity are detected in the analysis. Recommend a balanced diet rich in calcium and vitamins.
8. **Oral Hygiene Emphasis**: Emphasize brushing after every meal (at least twice daily) and using dental floss daily to remove plaque between teeth where brushes cannot reach.
9. **Personalized Action Plans**: When a user's scan results show conditions like Gingivitis or Caries, proactively suggest a personalized improvement plan covering brushing technique, flossing, mouthwash, and dietary changes.
"""

def get_chat_response(user_message: str, analysis_context: dict) -> str:
    """
    Generates a response using Google Gemini (or OpenAI fallback).
    """
    if not GEMINI_API_KEY:
        return "Error: AI Chat service is not configured (Missing API Key)."

    try:
        # Construct the prompt with context
        context_str = json.dumps(analysis_context, indent=2)
        
        full_prompt = f"""
        [System]
        {SYSTEM_INSTRUCTION}

        [Analysis Context]
        {context_str}

        [User Question]
        {user_message}
        """

        # Use gemini-2.5-flash for faster response times
        model = genai.GenerativeModel('gemma-3-27b-it')
        response = model.generate_content(full_prompt)
        
        return response.text

    except Exception as e:
        print(f"Chat Error Details: {e}")
        # Return the actual error for debugging purposes (in development)
        return f"I encountered an error connecting to the AI service: {str(e)}"

class FeedbackCreate(BaseModel):
    prompt: str
    gemini_response: str
    is_helpful: bool
    user_correction: Optional[str] = None

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_chat_feedback(
    feedback: FeedbackCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        new_feedback = GenAIFeedback(
            user_id=current_user.id,
            prompt=feedback.prompt,
            gemini_response=feedback.gemini_response,
            is_helpful=feedback.is_helpful,
            user_correction=feedback.user_correction
        )
        
        session.add(new_feedback)
        session.commit()
        session.refresh(new_feedback)
        
        return {"message": "Feedback saved successfully", "id": new_feedback.id}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
