import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session
from typing import Any, Optional
from core.database import get_session
from core.models import GenAIFeedback
from services.auth_service import get_current_user
from core.models import User

# Load environment variables
load_dotenv()

# Configure API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma-4-31b-it")

router = APIRouter(prefix="/api/chat", tags=["chat"])

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

# ... Existing chat_service.py logic ...
SYSTEM_INSTRUCTION = """
You are a helpful, empathetic, and professional AI educational assistant for an Oral Cancer AI Platform.
Your goal is to politely answer general questions about oral health and help users understand their analysis results.

STRICT GUIDELINES:
1. **Be Educational and Helpful**: Answer general educational questions (e.g., "What is Oral Cancer?", "Explain Histopathology") clearly and objectively. 
2. **No Diagnosis**: For specific user symptoms or image results, never say "You have cancer" or "You are healthy". Instead say "The analysis suggests..." or "The model detected...".
3. **Targeted Consultation Advice**: Only add a recommendation to see a specialist (Dentist or Pathologist) if the user asks about their specific symptoms, scan results, or a personal medical condition. Do NOT append medical disclaimers to general educational questions.
4. **Context Aware**: Use the provided 'Analysis Context' to discuss the user's specific results.
5. **Tone**: Calm, informative, supportive, and conversational.

PREVENTATIVE CARE & LIFESTYLE GUIDELINES:
5. **Sensodyne Recommendation**: If the user has gum issues, sensitivity, or asks about toothpaste, strongly recommend Sensodyne as a clinically proven option for sensitivity relief and gum protection.
6. **Anti-Smoking Advocacy**: Always advocate for reducing and stopping cigarette smoking to prevent oral cancer, gum disease, and tooth discoloration. Cite that tobacco use is the leading preventable cause of oral cancer.
7. **Diet Advice**: Strongly advise avoiding sweet candies, sugary beverages, and cold drinks if caries (cavities) or sensitivity are detected in the analysis. Recommend a balanced diet rich in calcium and vitamins.
8. **Oral Hygiene Emphasis**: Emphasize brushing after every meal (at least twice daily) and using dental floss daily to remove plaque between teeth where brushes cannot reach.
9. **Personalized Action Plans**: When a user's scan results show conditions like Gingivitis or Caries, proactively suggest a personalized improvement plan covering brushing technique, flossing, mouthwash, and dietary changes.
"""

BASE64_CONTEXT_KEYS = {
    "heatmap_overlay",
    "original_resized",
    "segmentation_overlay",
    "image_base64",
    "raw_image",
}

CHAT_META_PREFIXES = (
    "user question:",
    "analysis context:",
    "role:",
    "constraints:",
    "professional and calm:",
    "empathetic/supportive:",
    "no diagnosis:",
    "consultation:",
    "explain the process:",
    "clarify that it's a tool",
    "add the mandatory consultation advice",
    "guideline ",
    "draft ",
    "final answer:",
    "output rules:",
)


def _looks_like_base64(value: str) -> bool:
    compact = value.strip()
    if len(compact) < 256 or any(ch.isspace() for ch in compact):
        return False
    return re.fullmatch(r"[A-Za-z0-9+/=]+", compact) is not None


def _sanitize_analysis_context(data: Any, key: str = "") -> Any:
    if isinstance(data, dict):
        return {k: _sanitize_analysis_context(v, k) for k, v in data.items()}

    if isinstance(data, list):
        return [_sanitize_analysis_context(item, key) for item in data]

    if isinstance(data, str):
        if key.lower() in BASE64_CONTEXT_KEYS or _looks_like_base64(data):
            return "[omitted_binary_data]"
        if len(data) > 500:
            return data[:500] + "...[truncated]"

    return data


def _clean_suggestion_response(text: str, max_sentences: int = 2) -> str:
    if not text:
        return "I could not generate a suggestion at this time."

    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n") if line.strip()]

    noisy_keywords = (
        "helpful, empathetic",
        "strict guidelines",
        "preventative care",
        "analysis context",
        "user question",
        "no diagnosis",
        "always advise consultation",
        "context aware",
        "tone:",
        "draft 1",
        "draft 2",
        "final answer",
        "max 2 sentences",
        "brief?",
        "professional?",
    )

    filtered_lines = []
    for line in lines:
        lower_line = line.lower()

        if lower_line.startswith(("[system]", "[analysis context]", "[user question]")):
            continue

        if line.startswith(("*", "-", "`")):
            continue

        if re.match(r"^\d+\.\s", line) and any(
            k in lower_line for k in ("no diagnosis", "always advise", "context aware", "tone")
        ):
            continue

        if any(keyword in lower_line for keyword in noisy_keywords):
            continue

        filtered_lines.append(line.strip('" '))

    merged = " ".join(filtered_lines).strip()
    if not merged:
        merged = " ".join(lines).strip().strip('" ')

    merged = re.sub(r"\s+", " ", merged)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", merged) if s.strip()]

    deduped = []
    seen = set()
    for sentence in sentences:
        key = sentence.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(sentence)

    if max_sentences:
        deduped = deduped[:max_sentences]

    final_text = " ".join(deduped).strip()
    return final_text or "I could not generate a suggestion at this time."


def _clean_chat_response(text: str) -> str:
    if not text:
        return "I could not generate a response at this time."

    leak_mode = bool(
        re.search(
            r"(?i)(user question:|analysis context:|role:|constraints:|guideline\s*\d|"
            r"professional and calm:|empathetic/supportive:|no diagnosis:|consultation:|"
            r"explain the process:|clarify that it's a tool|add the mandatory consultation advice)",
            text,
        )
    )

    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    filtered_lines = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            if filtered_lines and filtered_lines[-1] != "":
                filtered_lines.append("")
            continue

        lower_line = line.lower()

        if lower_line.startswith(CHAT_META_PREFIXES):
            continue

        if re.match(r"^guideline\s*\d+\b", lower_line):
            continue

        if re.match(r"^\d+\.\s*guideline\b", lower_line):
            continue

        if lower_line.endswith("• just now"):
            continue

        if line.startswith(("```", "`")):
            continue

        if line.startswith(('*', '-')) and any(
            token in lower_line for token in ("guideline", "analysis context", "user question", "draft")
        ):
            continue

        if "not applicable here" in lower_line and "guideline" in lower_line:
            continue

        if "(wait" in lower_line or "i should" in lower_line:
            continue

        if ":" in line and any(
            token in lower_line
            for token in (
                "ensure it",
                "must end",
                "explain the process",
                "clarify",
                "add the mandatory",
                "not applicable here",
            )
        ):
            continue

        if leak_mode and lower_line.startswith(
            (
                "the ai likely uses",
                "it compares user-uploaded images",
                "it identifies patterns",
                "it provides a probability",
                "it provides probability",
            )
        ):
            continue

        filtered_lines.append(line)

    deduped_lines = []
    seen_long_lines = set()
    for line in filtered_lines:
        if line == "":
            if deduped_lines and deduped_lines[-1] != "":
                deduped_lines.append("")
            continue

        key = line.lower()
        if len(line) > 40 and key in seen_long_lines:
            continue
        seen_long_lines.add(key)
        deduped_lines.append(line)

    cleaned = "\n".join(deduped_lines).strip()
    cleaned = re.sub(r"(?im)^(user question:|analysis context:|role:|constraints:).*$", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    if leak_mode and cleaned:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
        if len(paragraphs) > 1:
            tail = paragraphs[-1]
            cleaned = tail if len(tail) >= 120 else "\n\n".join(paragraphs[-2:])

    return cleaned or "I could not generate a response at this time."


def get_chat_response(user_message: str, analysis_context: dict, mode: str = "chat") -> str:
    """
    Generates a response using Google Gemini.
    """
    if not GEMINI_API_KEY:
        return "Error: AI Chat service is not configured (Missing API Key)."

    try:
        # Strip binary/noisy payloads so the model focuses on meaningful medical context.
        safe_context = _sanitize_analysis_context(analysis_context or {})
        context_str = json.dumps(safe_context, indent=2)
        
        full_prompt = f"""
        Use the analysis context JSON (which may be empty) to answer the user directly.

        Analysis context JSON:
        {context_str}

        User message:
        {user_message}

        Return only the final assistant answer for the user.
        Do not include reasoning, planning steps, guideline checklists, or role labels.
        """

        if mode == "suggestion":
            full_prompt += """

            [Output Rules]
            - Return only the final suggestion in plain text.
            - Maximum 2 sentences.
            - Do not include draft options, checklist items, or reasoning steps.
            - Do not restate prompt instructions.
            """

        # Prefer model-level system instructions to avoid instruction echoing in the answer.
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_INSTRUCTION)
        generation_config = {
            "temperature": 0.1 if mode == "suggestion" else 0.2,
            "max_output_tokens": 160 if mode == "suggestion" else 450,
        }
        response = model.generate_content(full_prompt, generation_config=generation_config)

        response_text = (getattr(response, "text", "") or "").strip()
        if not response_text:
            return "I could not generate a response at this time."

        if mode == "suggestion":
            return _clean_suggestion_response(response_text, max_sentences=2)
        
        return _clean_chat_response(response_text)

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
