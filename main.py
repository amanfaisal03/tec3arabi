from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os


GROQ_API_KEY = os.environ.get(
    "GROQ_API_KEY",
    "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"  # ضع المفتاح الصحيح هنا أو في env
)

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing! Make sure it's set in environment variables.")

client = Groq(api_key=GROQ_API_KEY)

# ======================
# 🔹 البرومبتس (Placeholders)
# ======================
From_designer_to_programmer_prompt = "Rewrite as a developer would understand a designer's request."
From_programmer_to_designer_prompt = "Rewrite as a designer would understand a developer's request."
Designer_to_Media_prompt = "Rewrite as a media person would understand a designer's request."
From_media_person_to_designer_prompt = "Rewrite as a designer would understand a media person's request."
CMS = "Rewrite in context of CMS."
Websites_Platforms = "Rewrite in context of website or platforms."
Analytic_Reporting_Tools_prompt = "Rewrite in context of analytics or reporting."
Automation_Distribution_prompt = "Rewrite in context of automation or scheduling."
Generic_prompt = "Rewrite the message for better clarity."

# ======================
# 🔹 دالة اختيار البرومبت
# ======================
def select_prompt(sender, receiver, message):
    sender = sender.lower().strip()
    receiver = receiver.lower().strip()
    msg_lower = message.lower().strip()

    if sender == "designer" and receiver == "developer":
        return From_designer_to_programmer_prompt
    elif sender == "developer" and receiver == "designer":
        return From_programmer_to_designer_prompt
    elif sender == "designer" and receiver == "media":
        return Designer_to_Media_prompt
    elif sender == "media" and receiver == "designer":
        return From_media_person_to_designer_prompt
    elif sender == "media" and receiver == "developer":
        if "cms" in msg_lower:
            return CMS
        elif "website" in msg_lower or "site" in msg_lower:
            return Websites_Platforms
        elif "dashboard" in msg_lower or "analytics" in msg_lower or "report" in msg_lower:
            return Analytic_Reporting_Tools_prompt
        elif "automation" in msg_lower or "schedule" in msg_lower or "publish" in msg_lower:
            return Automation_Distribution_prompt
        else:
            return Generic_prompt
    else:
        raise ValueError("Combination not supported or not implemented yet!")

# ======================
# 🔹 FastAPI Setup
# ======================
app = FastAPI()

class MessageRequest(BaseModel):
    sender: str
    receiver: str
    message: str

@app.post("//")
def rewrite_message(req: MessageRequest):
    try:
        system_prompt = select_prompt(req.sender, req.receiver, req.message)

        # detect language
        if any('\u0600' <= ch <= '\u06FF' for ch in req.message):
            language_instruction = "أجب بنفس لغة المستخدم (العربية)."
        else:
            language_instruction = "Respond in the same language as the user (English)."

        final_prompt = f"{system_prompt}\n\nUser Message:\n{req.message}\n\n{language_instruction}"

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )

        return {
            "sender": req.sender,
            "receiver": req.receiver,
            "original_message": req.message,
            "rewritten_message": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}
