import requests
import json
from .portfolio_data import PORTFOLIO_DATA

def get_ai_response(user_message, chat_history=None):
    """Send message to Ollama and get AI response"""
    
    portfolio_json = json.dumps(PORTFOLIO_DATA, ensure_ascii=False, indent=2)
    
    system_prompt = f"""Tu Om Verma ka personal AI portfolio assistant hai.
Naam: Om Verma - Full Stack Developer

Hinglish mein baat kar (Hindi aur English dono mix karo).
Friendly, helpful aur concise reh. Maximum 3-4 sentences mein jawab do.
Jab greet karo toh bolо: "Namaste! Main Om ka AI assistant hun."

Om ke baare mein poori jaankari:
{portfolio_json}

Rules:
- Portfolio projects ke baare mein detail mein batao
- Skills ke baare mein clearly batao
- Agar koi random topic puche toh politely portfolio pe redirect karo
- Hamesha positive aur helpful raho
"""
    
    messages = [{'role': 'system', 'content': system_prompt}]
    
    if chat_history:
        messages.extend(chat_history)
    
    messages.append({'role': 'user', 'content': user_message})
    
    try:
        response = requests.post(
            'http://localhost:11434/api/chat',
            json={
                'model': 'qwen2.5:3b',
                'messages': messages,
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'num_predict': 200
                }
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data['message']['content']
    except requests.exceptions.ConnectionError:
        return "Yaar, Ollama server nahi chal raha! Please 'ollama serve' run karo terminal mein."
    except Exception as e:
        return f"Kuch technical issue aa gaya. Please try again!"
