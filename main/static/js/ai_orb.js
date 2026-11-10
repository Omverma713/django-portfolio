/**
 * AI Orb - Om Verma Portfolio Assistant
 * Voice-powered AI assistant with animated Three.js orb
 * Features: Welcome intro overlay + floating corner orb
 */

const AIOrb = {
    // Three.js - Intro (big)
    introScene: null, introCam: null, introRenderer: null, introMesh: null,
    introLight1: null, introLight2: null,

    // Three.js - Corner (small)
    cornerScene: null, cornerCam: null, cornerRenderer: null, cornerMesh: null,

    // State
    isListening: false,
    isSpeaking: false,
    isThinking: false,
    isPanelOpen: false,
    chatHistory: [],
    currentAudio: null,
    recognition: null,

    init() {
        this.createIntroOverlay();
        this.createCornerWidget();
        this.initIntroThreeJS();
        this.initCornerThreeJS();
        this.initSpeechRecognition();
        this.animate();
        this.setupEvents();
        this.playWelcome();
    },

    /* ==================== INTRO OVERLAY ==================== */
    createIntroOverlay() {
        const html = `
        <div id="ai-intro-overlay">
            <div id="ai-intro-content">
                <!-- Big 3D Orb -->
                <div id="ai-intro-orb-wrap">
                    <canvas id="ai-intro-canvas"></canvas>
                    <div id="ai-intro-ring1"></div>
                    <div id="ai-intro-ring2"></div>
                    <div id="ai-intro-glow"></div>
                </div>

                <!-- Greeting Text -->
                <div id="ai-intro-text">
                    <h2 id="ai-intro-hello">Namaste! 👋</h2>
                    <p id="ai-intro-msg">Main <strong>Om Verma</strong> ka AI Assistant hun.</p>
                    <p id="ai-intro-question">Main kya help kar sakta hun aapki?</p>
                </div>

                <!-- Action Buttons -->
                <div id="ai-intro-actions">
                    <button id="ai-intro-mic-btn">🎙️ Voice se baat karo</button>
                    <button id="ai-intro-type-btn">💬 Type karo</button>
                </div>

                <!-- Skip / Close -->
                <button id="ai-intro-close" title="Website dekho">
                    <span>✕</span>
                    <small>Website dekho</small>
                </button>
            </div>
        </div>`;

        document.body.insertAdjacentHTML('afterbegin', html);
    },

    /* ==================== CORNER WIDGET ==================== */
    createCornerWidget() {
        const html = `
        <div id="ai-orb-widget">
            <!-- Floating Corner Orb -->
            <div id="ai-orb-float" title="Om ke AI Assistant se baat karo">
                <canvas id="ai-orb-canvas"></canvas>
                <div id="ai-orb-pulse"></div>
                <div id="ai-orb-tooltip">AI Assistant</div>
            </div>

            <!-- Chat Panel -->
            <div id="ai-orb-panel">
                <div id="ai-orb-header">
                    <div id="ai-orb-avatar"><span>AI</span></div>
                    <div>
                        <div id="ai-orb-name">Om's Assistant</div>
                        <div id="ai-orb-online">● Online</div>
                    </div>
                    <button id="ai-orb-close">✕</button>
                </div>

                <div id="ai-orb-messages">
                    <div class="ai-msg ai-msg-bot">
                        <span>Wapas aa gaye! 😊 Kuch aur poochna hai toh batao.</span>
                    </div>
                </div>

                <div id="ai-orb-status-bar" class="hidden">
                    <div id="ai-orb-dots"><span></span><span></span><span></span></div>
                    <span id="ai-orb-status-label">Sun raha hun...</span>
                </div>

                <div id="ai-orb-input-area">
                    <input type="text" id="ai-orb-input" placeholder="Kuch bhi pucho..." />
                    <button id="ai-orb-send" title="Send">➤</button>
                    <button id="ai-orb-mic" title="Voice">🎙️</button>
                </div>
            </div>
        </div>`;

        document.body.insertAdjacentHTML('beforeend', html);
    },

    /* ==================== THREE.JS - INTRO (BIG) ==================== */
    initIntroThreeJS() {
        const canvas = document.getElementById('ai-intro-canvas');
        this.introScene = new THREE.Scene();
        this.introCam = new THREE.PerspectiveCamera(55, 1, 0.1, 100);
        this.introCam.position.z = 2.8;

        this.introRenderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
        this.introRenderer.setSize(260, 260);
        this.introRenderer.setPixelRatio(window.devicePixelRatio);
        this.introRenderer.setClearColor(0x000000, 0);

        // Main sphere
        const mat = new THREE.MeshPhongMaterial({
            color: 0x6c63ff,
            emissive: 0x2d1b69,
            specular: 0xffffff,
            shininess: 150,
            transparent: true,
            opacity: 0.93,
        });
        this.introMesh = new THREE.Mesh(new THREE.SphereGeometry(0.85, 64, 64), mat);
        this.introScene.add(this.introMesh);

        // Wireframe
        const wireMat = new THREE.MeshBasicMaterial({ color: 0xb0aaff, wireframe: true, transparent: true, opacity: 0.06 });
        const wire = new THREE.Mesh(new THREE.SphereGeometry(0.87, 18, 18), wireMat);
        this.introScene.add(wire);
        this.introWire = wire;

        // Lights
        this.introScene.add(new THREE.AmbientLight(0x404040, 3));
        this.introLight1 = new THREE.PointLight(0x6c63ff, 5, 15);
        this.introLight1.position.set(2, 2, 2);
        this.introScene.add(this.introLight1);
        this.introLight2 = new THREE.PointLight(0x00d4ff, 2.5, 15);
        this.introLight2.position.set(-2, -1, 1);
        this.introScene.add(this.introLight2);
    },

    /* ==================== THREE.JS - CORNER (SMALL) ==================== */
    initCornerThreeJS() {
        const canvas = document.getElementById('ai-orb-canvas');
        this.cornerScene = new THREE.Scene();
        this.cornerCam = new THREE.PerspectiveCamera(60, 1, 0.1, 100);
        this.cornerCam.position.z = 2.5;

        this.cornerRenderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
        this.cornerRenderer.setSize(70, 70);
        this.cornerRenderer.setPixelRatio(window.devicePixelRatio);
        this.cornerRenderer.setClearColor(0x000000, 0);

        const mat = new THREE.MeshPhongMaterial({
            color: 0x6c63ff, emissive: 0x2d1b69,
            specular: 0xffffff, shininess: 120,
            transparent: true, opacity: 0.92,
        });
        this.cornerMesh = new THREE.Mesh(new THREE.SphereGeometry(0.75, 64, 64), mat);
        this.cornerScene.add(this.cornerMesh);

        this.cornerScene.add(new THREE.AmbientLight(0x404040, 3));
        const cLight = new THREE.PointLight(0x6c63ff, 4, 10);
        cLight.position.set(2, 2, 2);
        this.cornerScene.add(cLight);
        this.cornerLight = cLight;
    },

    /* ==================== WELCOME SPEECH ==================== */
    async playWelcome() {
        // Small delay then speak welcome
        await this.delay(1200);
        const welcomeText = "Namaste! Main Om Verma ka AI assistant hun. Main aapki kya help kar sakta hun?";
        this.isSpeaking = true;
        try {
            const response = await fetch('/ai/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': this.getCookie('csrftoken') },
                body: JSON.stringify({ message: '__welcome__', history: [] }),
            });
            const data = await response.json();
            if (data.audio) {
                const audio = new Audio('data:audio/mp3;base64,' + data.audio);
                this.currentAudio = audio;
                audio.play().catch(() => {});
                audio.onended = () => { this.isSpeaking = false; };
            }
        } catch(e) {
            this.isSpeaking = false;
        }
    },

    /* ==================== EVENTS ==================== */
    setupEvents() {
        // Intro close
        document.getElementById('ai-intro-close').addEventListener('click', () => this.closeIntro());

        // Intro mic button
        document.getElementById('ai-intro-mic-btn').addEventListener('click', () => {
            this.closeIntro();
            setTimeout(() => this.startRecording(), 600);
        });

        // Intro type button
        document.getElementById('ai-intro-type-btn').addEventListener('click', () => {
            this.closeIntro();
            setTimeout(() => this.openPanel(), 500);
        });

        // Corner orb click -> toggle panel
        document.getElementById('ai-orb-float').addEventListener('click', () => this.togglePanel());

        // Close panel
        document.getElementById('ai-orb-close').addEventListener('click', () => this.togglePanel(false));

        // Send
        document.getElementById('ai-orb-send').addEventListener('click', () => {
            const input = document.getElementById('ai-orb-input');
            const text = input.value.trim();
            if (text) { this.sendMessage(text); input.value = ''; }
        });

        // Enter key
        document.getElementById('ai-orb-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const text = e.target.value.trim();
                if (text) { this.sendMessage(text); e.target.value = ''; }
            }
        });

        // Mic button - toggle recording
        document.getElementById('ai-orb-mic').addEventListener('click', () => {
            if (this.isListening) this.stopRecording();
            else this.startRecording();
        });
    },

    closeIntro() {
        const overlay = document.getElementById('ai-intro-overlay');
        overlay.classList.add('closing');
        if (this.currentAudio) { this.currentAudio.pause(); this.isSpeaking = false; }
        setTimeout(() => { overlay.style.display = 'none'; }, 600);
    },

    openPanel() {
        this.isPanelOpen = true;
        document.getElementById('ai-orb-panel').classList.add('open');
        setTimeout(() => document.getElementById('ai-orb-input').focus(), 300);
    },

    togglePanel(forceOpen) {
        this.isPanelOpen = forceOpen !== undefined ? forceOpen : !this.isPanelOpen;
        document.getElementById('ai-orb-panel').classList.toggle('open', this.isPanelOpen);
        if (this.isPanelOpen) setTimeout(() => document.getElementById('ai-orb-input').focus(), 300);
    },

    /* ==================== SPEECH RECOGNITION (Faster-Whisper) ==================== */
    initSpeechRecognition() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.warn('❌ MediaRecorder not supported!');
            return;
        }
        this.mediaRecorder = null;
        this.audioChunks = [];
        console.log('✅ MediaRecorder ready — using Faster-Whisper backend');
    },

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });
            this.audioChunks = [];
            this.activeStream = stream;

            const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
                ? 'audio/webm;codecs=opus'
                : MediaRecorder.isTypeSupported('audio/webm')
                ? 'audio/webm'
                : 'audio/ogg';

            this.mediaRecorder = new MediaRecorder(stream, { mimeType });

            this.mediaRecorder.ondataavailable = (e) => {
                if (e.data && e.data.size > 0) this.audioChunks.push(e.data);
            };

            this.mediaRecorder.onstop = async () => {
                if (this.activeStream) {
                    this.activeStream.getTracks().forEach(t => t.stop());
                }

                const audioBlob = new Blob(this.audioChunks, { type: mimeType });
                console.log(`🎙️ Audio recorded: ${(audioBlob.size / 1024).toFixed(1)} KB`);

                if (audioBlob.size < 500) {
                    this.addMessage('bot', '🤫 Kuch suna nahi. Mic ke paas aakar boliye!');
                    this.setStatus('', false);
                    this.isListening = false;
                    document.getElementById('ai-orb-mic').textContent = '🎙️';
                    return;
                }

                await this.transcribeAudio(audioBlob);
            };

            this.mediaRecorder.start(200);
            this.isListening = true;
            this.setStatus('Sun raha hun... 🎙️ (Bol kar dobara mic dabayein)', true);
            document.getElementById('ai-orb-mic').textContent = '⏹️';
            console.log('🎙️ Recording started with enhanced audio...');
            if (!this.isPanelOpen) this.openPanel();

        } catch (err) {
            console.error('Mic error:', err);
            if (err.name === 'NotAllowedError') {
                this.addMessage('bot', '🔒 Mic permission denied! Browser address bar mein mic allow karein.');
            } else {
                this.addMessage('bot', '🎤 Mic connect nahi ho paya: ' + err.message);
            }
        }
    },

    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
            this.setStatus('AI samajh raha hai... ⏳', true);
            document.getElementById('ai-orb-mic').textContent = '🎙️';
            console.log('⏹️ Recording stopped');
        }
        this.isListening = false;
    },

    // Convert WebM blob → WAV using Web Audio API (no ffmpeg needed!)
    async blobToWav(webmBlob) {
        const arrayBuffer = await webmBlob.arrayBuffer();
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
        await audioCtx.close();

        // Get mono channel data at 16kHz
        const channelData = audioBuffer.getChannelData(0);
        const sampleRate = audioBuffer.sampleRate;

        // Encode as 16-bit PCM WAV
        const numSamples = channelData.length;
        const wavBuffer = new ArrayBuffer(44 + numSamples * 2);
        const view = new DataView(wavBuffer);

        const writeStr = (offset, str) => {
            for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
        };

        writeStr(0,  'RIFF');
        view.setUint32(4,  36 + numSamples * 2, true);
        writeStr(8,  'WAVE');
        writeStr(12, 'fmt ');
        view.setUint32(16, 16, true);       // chunk size
        view.setUint16(20, 1,  true);       // PCM format
        view.setUint16(22, 1,  true);       // mono
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2,  true);       // block align
        view.setUint16(34, 16, true);       // bits per sample
        writeStr(36, 'data');
        view.setUint32(40, numSamples * 2, true);

        // Write PCM samples (clamp to [-1, 1])
        for (let i = 0; i < numSamples; i++) {
            const s = Math.max(-1, Math.min(1, channelData[i]));
            view.setInt16(44 + i * 2, s * 0x7FFF, true);
        }

        return new Blob([wavBuffer], { type: 'audio/wav' });
    },

    async transcribeAudio(webmBlob) {
        try {
            // Convert to WAV first (works without ffmpeg!)
            let audioBlob;
            try {
                console.log('🔄 Converting WebM → WAV...');
                audioBlob = await this.blobToWav(webmBlob);
                console.log(`✅ WAV: ${(audioBlob.size/1024).toFixed(1)} KB`);
            } catch (convErr) {
                console.warn('WAV conversion failed, sending webm:', convErr);
                audioBlob = webmBlob;
            }

            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');

            const res = await fetch('/ai/transcribe/', {
                method: 'POST',
                headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
                body: formData,
            });

            const data = await res.json();
            console.log('📝 Transcribed:', data.text);

            if (data.text && data.text.trim()) {
                document.getElementById('ai-orb-input').value = data.text;
                this.sendMessage(data.text);
            } else {
                this.addMessage('bot', '🤫 Kuch samajh nahi aaya. Thoda aur paas se clearly bolo!');
                this.setStatus('', false);
            }
        } catch (err) {
            console.error('Transcribe error:', err);
            this.addMessage('bot', 'Transcription mein error. Server chal raha hai?');
            this.setStatus('', false);
        }
    },


    /* ==================== SEND MESSAGE ==================== */
    async sendMessage(text) {
        if (this.isThinking) return;
        if (this.currentAudio) { this.currentAudio.pause(); this.currentAudio = null; }
        this.addMessage('user', text);
        document.getElementById('ai-orb-input').value = '';
        this.isThinking = true;
        this.setStatus('Soch raha hun... 🤔', true);

        try {
            const res = await fetch('/ai/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': this.getCookie('csrftoken') },
                body: JSON.stringify({ message: text, history: this.chatHistory.slice(-6) }),
            });
            const data = await res.json();
            this.addMessage('bot', data.text);
            this.chatHistory.push({ role: 'user', content: text });
            this.chatHistory.push({ role: 'assistant', content: data.text });

            if (data.audio) {
                this.setStatus('Bol raha hun... 🔊', true);
                this.isSpeaking = true;
                const audio = new Audio('data:audio/mp3;base64,' + data.audio);
                this.currentAudio = audio;
                audio.play().catch(() => {});
                audio.onended = () => { this.isSpeaking = false; this.setStatus('', false); };
            } else {
                this.setStatus('', false);
            }
        } catch (err) {
            this.addMessage('bot', 'Server se connect nahi ho pa raha. Ollama chal raha hai?');
            this.setStatus('', false);
        }
        this.isThinking = false;
    },

    /* ==================== HELPERS ==================== */
    addMessage(type, text) {
        const messages = document.getElementById('ai-orb-messages');
        const div = document.createElement('div');
        div.className = `ai-msg ai-msg-${type}`;
        div.innerHTML = `<span>${this.escapeHtml(text)}</span>`;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    },

    setStatus(text, show) {
        const bar = document.getElementById('ai-orb-status-bar');
        bar.classList.toggle('hidden', !show);
        if (text) document.getElementById('ai-orb-status-label').textContent = text;
    },

    escapeHtml(t) {
        return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
    },

    getCookie(name) {
        return document.cookie.split(';').find(c => c.trim().startsWith(name+'='))?.split('=')[1] || '';
    },

    delay(ms) { return new Promise(r => setTimeout(r, ms)); },

    /* ==================== ANIMATION LOOP ==================== */
    animate() {
        requestAnimationFrame(() => this.animate());
        const t = Date.now() * 0.001;

        // State colors
        let color = 0x6c63ff, emissive = 0x2d1b69, scale = 1;

        if (this.isListening) {
            color = 0xff4444; emissive = 0x8b0000;
            scale = 1 + Math.sin(t * 8) * 0.13;
        } else if (this.isThinking) {
            color = 0xaa44ff; emissive = 0x4a0080;
            scale = 1 + Math.sin(t * 4) * 0.07;
        } else if (this.isSpeaking) {
            color = 0x00cc66; emissive = 0x004d00;
            scale = 1 + Math.sin(t * 10) * 0.11;
        } else {
            scale = 1 + Math.sin(t * 1.5) * 0.03;
        }

        // Animate INTRO orb
        if (this.introMesh) {
            this.introMesh.rotation.y += 0.008;
            this.introMesh.rotation.x = Math.sin(t * 0.4) * 0.08;
            this.introMesh.scale.setScalar(scale);
            this.introMesh.material.color.setHex(color);
            this.introMesh.material.emissive.setHex(emissive);
            if (this.introWire) this.introWire.rotation.y -= 0.004;
            this.introRenderer.render(this.introScene, this.introCam);
        }

        // Animate CORNER orb
        if (this.cornerMesh) {
            this.cornerMesh.rotation.y += 0.01;
            this.cornerMesh.scale.setScalar(scale);
            this.cornerMesh.material.color.setHex(color);
            this.cornerMesh.material.emissive.setHex(emissive);
            this.cornerRenderer.render(this.cornerScene, this.cornerCam);
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    if (typeof THREE !== 'undefined') AIOrb.init();
    else console.error('Three.js not loaded!');
});
