import os
from groq import Groq 
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing! Make sure it's set in environment variables.")

client = Groq(api_key=GROQ_API_KEY)  



def select_prompt(sender, receiver,message):
    sender = sender.lower().strip()
    receiver = receiver.lower().strip()
    msg_lower = message.lower().strip()
    if sender == "designer"  and receiver == "developer":
        return From_designer_to_programmer_prompt
    elif sender == "developer" and receiver == "designer":
        return From_programmer_to_designer_prompt
    elif sender == "designer" and receiver == "media":
        return Designer_to_Media_prompt
    elif sender == "media" and receiver == "designer":
        return From_media_person_to_designer_prompt
    if sender == "media" and receiver == "developer":
        msg_lower = message.lower()
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
    

sender = input("Enter sender (designer/developer/media): ").strip().lower()
receiver = input("Enter receiver (designer/developer/media): ").strip().lower()
user_input = input("Enter your message: ").strip()

system_prompt = select_prompt(sender, receiver, user_input)

if any('\u0600' <= ch <= '\u06FF' for ch in user_input):
         language_instruction = "أجب بنفس لغة المستخدم (العربية)."
else:     
       language_instruction = "Respond in the same language as the user (English)."

final_prompt = f"{system_prompt}\n\nUser Message:\n{user_input}\n\n{language_instruction}"

response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": final_prompt}
    ],
    model="llama-3.3-70b-versatile",
    temperature=0.0
)


print("\n--- Final Response ---\n")
print(response.choices[0].message.content) 