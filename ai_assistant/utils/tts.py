try:
    import edge_tts
except ImportError:
    edge_tts = None
import asyncio
import tempfile
import base64
import os

async def _generate_speech(text: str) -> bytes:
    """Generate speech audio bytes from text using Edge TTS"""
    if edge_tts is None:
        return b""
    communicate = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural", rate="+5%")
    
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        tmp_path = f.name
    
    try:
        await communicate.save(tmp_path)
        with open(tmp_path, 'rb') as f:
            return f.read()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def text_to_speech(text: str) -> str:
    """Convert text to speech, return base64 encoded audio string"""
    try:
        # Clean text for TTS (remove emojis and markdown)
        import re
        clean_text = re.sub(r'[*_#\[\]()~]', '', text)
        clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', clean_text)
        clean_text = clean_text.strip()
        
        if not clean_text:
            return ""
        
        audio_bytes = asyncio.run(_generate_speech(clean_text))
        return base64.b64encode(audio_bytes).decode('utf-8')
    except Exception as e:
        print(f"TTS Error: {e}")
        return ""
