import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils.ollama_chat import get_ai_response
from .utils.tts import text_to_speech
from .utils.stt import transcribe_audio

WELCOME_TEXT = "Namaste! Main Om Verma ka AI assistant hun. Aap mujhse Om ke projects, skills, ya kisi bhi cheez ke baare mein pooch sakte hain. Main aapki kya help kar sakta hun?"

@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    """Main chat endpoint - receives text, returns AI response + audio"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        chat_history = data.get('history', [])

        # Special welcome message on page load
        if user_message == '__welcome__':
            audio_base64 = text_to_speech(WELCOME_TEXT)
            return JsonResponse({'text': WELCOME_TEXT, 'audio': audio_base64, 'status': 'success'})

        if not user_message:
            return JsonResponse({'error': 'Message required'}, status=400)

        # Get AI text response from Ollama
        ai_text = get_ai_response(user_message, chat_history)

        # Convert AI response to speech (Edge TTS)
        audio_base64 = text_to_speech(ai_text)

        return JsonResponse({
            'text': ai_text,
            'audio': audio_base64,
            'status': 'success'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'text': 'Kuch error aa gaya, please try again!',
            'audio': '',
            'status': 'error'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def transcribe(request):
    """Voice endpoint - receives audio blob, returns transcribed text"""
    try:
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return JsonResponse({'error': 'No audio file'}, status=400)

        audio_bytes = audio_file.read()
        print(f"[Transcribe Endpoint] Received audio: {len(audio_bytes)} bytes, name: {audio_file.name}")

        # Save for inspection
        with open('last_recording.wav', 'wb') as f:
            f.write(audio_bytes)

        # Transcribe with Faster-Whisper
        text = transcribe_audio(audio_bytes)
        print(f"[Transcribe Endpoint] Transcription output: '{text}'")

        if not text:
            return JsonResponse({'text': '', 'status': 'no_speech'})

        return JsonResponse({'text': text, 'status': 'success'})

    except Exception as e:
        print(f"[Transcribe Endpoint] Error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e), 'text': '', 'status': 'error'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Check if AI assistant is running"""
    import requests as req
    try:
        response = req.get('http://localhost:11434/api/tags', timeout=3)
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]
        return JsonResponse({
            'status': 'ok',
            'ollama': 'running',
            'models': model_names
        })
    except:
        return JsonResponse({
            'status': 'warning',
            'ollama': 'not running',
            'message': 'Please run: ollama serve'
        })
