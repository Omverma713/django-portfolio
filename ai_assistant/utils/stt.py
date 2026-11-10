import os
import tempfile
import threading
try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

_model = None
_model_lock = threading.Lock()

def get_model():
    global _model
    if WhisperModel is None:
        return None
    if _model is not None:
        return _model
    with _model_lock:
        if _model is None:
            try:
                print("[Whisper] Loading 'base' model...")
                _model = WhisperModel("base", device="cpu", compute_type="int8")
                print("[Whisper] 'base' model ready!")
            except Exception as e:
                print(f"[Whisper] Failed to load model: {e}")
                return None
    return _model

def transcribe_audio(audio_bytes: bytes, language: str = None) -> str:
    try:
        model = get_model()
        if model is None:
            return "STT model unavailable on this server."

        # Check format
        if audio_bytes.startswith(b'RIFF'):
            suffix = '.wav'
        elif audio_bytes.startswith(b'\x1aE\xdf\xa3'):
            suffix = '.webm'
        elif audio_bytes.startswith(b'OggS'):
            suffix = '.ogg'
        else:
            suffix = '.wav'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name

        try:
            print(f"[Whisper] Processing file: {tmp_path} ({len(audio_bytes)} bytes)")
            segments, info = model.transcribe(
                tmp_path,
                language=language,
                beam_size=5,
                vad_filter=False,
                temperature=[0.0, 0.2, 0.4]
            )
            text_parts = [seg.text for seg in segments]
            text = " ".join(text_parts).strip()
            print(f"[Whisper] Detected lang: {info.language} ({info.language_probability:.2f}), Text: '{text}'")
            return text

        finally:
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    except Exception as e:
        print(f"[Whisper] Transcribe error: {e}")
        import traceback
        traceback.print_exc()
        return ""

# Pre-load base model
threading.Thread(target=get_model, daemon=True).start()
