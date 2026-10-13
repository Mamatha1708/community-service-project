/**
 * Kalamkari Mitra Multilingual Voice & Speech Assistant
 * Supports Telugu (te-IN), Hindi (hi-IN), and English (en-IN).
 * Uses browser Web Speech API (SpeechRecognition) & SpeechSynthesis with graceful fallback.
 */

class KalamkariVoiceAssistant {
  constructor(options = {}) {
    this.currentLanguage = options.language || 'en-IN';
    this.recognition = null;
    this.isListening = false;
    this.synth = window.speechSynthesis || null;
    this.currentUtterance = null;
    this.uiStrings = options.uiStrings || {};

    // Elements
    this.micBtn = document.getElementById(options.micBtnId || 'micToggleBtn');
    this.micStatus = document.getElementById(options.micStatusId || 'micStatusIndicator');
    this.inputBox = document.getElementById(options.inputBoxId || 'voiceInputBox');
    this.sendBtn = document.getElementById(options.sendBtnId || 'voiceSendBtn');
    this.chatContainer = document.getElementById(options.chatContainerId || 'chatMessagesContainer');
    this.langSelect = document.getElementById(options.langSelectId || 'langSelector');
    this.stopAudioBtn = document.getElementById(options.stopAudioBtnId || 'stopAudioBtn');
    this.alertBox = document.getElementById(options.alertBoxId || 'voiceAlertBox');

    this.initRecognition();
    this.bindEvents();
  }

  initRecognition() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
      this.recognition = new SpeechRec();
      this.recognition.continuous = false; // Stop when user pauses speaking (avoids infinite recording)
      this.recognition.interimResults = true;
      this.recognition.lang = this.currentLanguage;

      this.recognition.onstart = () => {
        this.isListening = true;
        this.updateMicUI(true);
        this.showAlert(null);
      };

      this.recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          transcript += event.results[i][0].transcript;
        }
        if (this.inputBox) {
          this.inputBox.value = transcript;
        }
      };

      this.recognition.onerror = (event) => {
        console.warn('Speech recognition event error:', event.error);
        this.stopListening();
        let msg = 'Recognition error. Please type your query.';
        if (event.error === 'not-allowed') {
          msg = this.uiStrings.mic_permission_denied || 'Microphone access denied. Please grant permission in browser.';
        } else if (event.error === 'no-speech') {
          msg = this.uiStrings.recognition_error || 'No speech detected. Please speak closer to microphone.';
        }
        this.showAlert(msg, 'warning');
      };

      this.recognition.onend = () => {
        this.stopListening();
      };
    } else {
      console.warn('Web Speech API is not natively supported in this browser.');
    }
  }

  bindEvents() {
    // Mic button toggle
    if (this.micBtn) {
      this.micBtn.addEventListener('click', () => {
        if (this.isListening) {
          this.stopListening();
        } else {
          this.startListening();
        }
      });
    }

    // Send button
    if (this.sendBtn) {
      this.sendBtn.addEventListener('click', () => {
        this.sendQuery();
      });
    }

    // Enter key submit in input box
    if (this.inputBox) {
      this.inputBox.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendQuery();
        }
      });
    }

    // Language select
    if (this.langSelect) {
      this.langSelect.addEventListener('change', (e) => {
        this.setLanguage(e.target.value);
      });
    }

    // Stop audio speech
    if (this.stopAudioBtn) {
      this.stopAudioBtn.addEventListener('click', () => {
        this.stopSpeaking();
      });
    }
  }

  startListening() {
    if (!this.recognition) {
      const msg = this.uiStrings.speech_unsupported || 'Voice recognition not supported in this browser. Please type your query.';
      this.showAlert(msg, 'info');
      return;
    }

    this.stopSpeaking(); // Silence any audio output first

    try {
      this.recognition.lang = this.currentLanguage;
      this.recognition.start();
    } catch (err) {
      console.warn('Recognition start exception:', err);
    }
  }

  stopListening() {
    this.isListening = false;
    this.updateMicUI(false);
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
    }
  }

  updateMicUI(listening) {
    if (!this.micBtn) return;
    if (listening) {
      this.micBtn.classList.remove('btn-outline-danger');
      this.micBtn.classList.add('btn-danger', 'pulse-animation');
      this.micBtn.innerHTML = '<i class="bi bi-mic-fill me-1"></i> ' + (this.uiStrings.mic_listening || 'Listening...');
      if (this.micStatus) {
        this.micStatus.style.display = 'inline-block';
      }
    } else {
      this.micBtn.classList.remove('btn-danger', 'pulse-animation');
      this.micBtn.classList.add('btn-outline-danger');
      this.micBtn.innerHTML = '<i class="bi bi-mic me-1"></i> ' + (this.uiStrings.mic_start || 'Start Speaking');
      if (this.micStatus) {
        this.micStatus.style.display = 'none';
      }
    }
  }

  setLanguage(langCode) {
    this.currentLanguage = langCode;
    if (this.recognition) {
      this.recognition.lang = langCode;
    }
    // Fetch localized UI strings from server
    fetch(`/api/voice-assistant/strings?lang=${encodeURIComponent(langCode)}`)
      .then(r => r.json())
      .then(strings => {
        this.uiStrings = strings;
        this.applyUIStrings();
      })
      .catch(err => console.error(err));
  }

  applyUIStrings() {
    if (this.inputBox && this.uiStrings.input_placeholder) {
      this.inputBox.placeholder = this.uiStrings.input_placeholder;
    }
    if (this.micBtn && !this.isListening && this.uiStrings.mic_start) {
      this.micBtn.innerHTML = `<i class="bi bi-mic me-1"></i> ${this.uiStrings.mic_start}`;
    }
    if (this.sendBtn && this.uiStrings.send_button) {
      this.sendBtn.innerHTML = `<i class="bi bi-send-fill me-1"></i> ${this.uiStrings.send_button}`;
    }
  }

  sendQuery(queryText = null) {
    const text = (queryText !== null ? queryText : (this.inputBox ? this.inputBox.value : '')).trim();
    if (!text) return;

    this.stopListening();
    this.stopSpeaking();

    // Add user message to chat UI
    this.appendMessage('user', text);
    if (this.inputBox) {
      this.inputBox.value = '';
    }

    // Show typing loader
    const loadingId = this.appendLoadingMessage();

    fetch('/api/voice-assistant/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: text,
        language: this.currentLanguage
      })
    })
    .then(r => r.json())
    .then(resp => {
      this.removeLoadingMessage(loadingId);
      if (resp.success) {
        this.appendMessage('assistant', resp.reply, resp.action_url, resp.action_label);
        // Automatically speak response
        this.speakText(resp.reply);
      } else {
        this.appendMessage('assistant', resp.reply || 'Sorry, I could not process your request.');
      }
    })
    .catch(err => {
      this.removeLoadingMessage(loadingId);
      console.error(err);
      this.appendMessage('assistant', 'Network issue. Please check your connection and try again.');
    });
  }

  speakText(text) {
    if (!this.synth) {
      console.warn('Speech synthesis unsupported in this browser.');
      return;
    }

    this.synth.cancel(); // Stop any pending speech

    // Clean markdown/newlines for speech
    const cleanSpeech = text.replace(/[*_#]/g, '').replace(/\n/g, '. ');
    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.lang = this.currentLanguage;
    utterance.rate = 0.95; // Slightly measured pace for clarity

    // Try finding matching voice
    const voices = this.synth.getVoices();
    const langPrefix = this.currentLanguage.split('-')[0];
    const matchVoice = voices.find(v => v.lang === this.currentLanguage || v.lang.startsWith(langPrefix));
    if (matchVoice) {
      utterance.voice = matchVoice;
    }

    if (this.stopAudioBtn) {
      this.stopAudioBtn.style.display = 'inline-block';
    }

    utterance.onend = () => {
      if (this.stopAudioBtn) {
        this.stopAudioBtn.style.display = 'none';
      }
    };

    utterance.onerror = () => {
      if (this.stopAudioBtn) {
        this.stopAudioBtn.style.display = 'none';
      }
    };

    this.currentUtterance = utterance;
    this.synth.speak(utterance);
  }

  stopSpeaking() {
    if (this.synth) {
      this.synth.cancel();
    }
    if (this.stopAudioBtn) {
      this.stopAudioBtn.style.display = 'none';
    }
  }

  appendMessage(sender, text, actionUrl = null, actionLabel = null) {
    if (!this.chatContainer) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `d-flex mb-3 ${sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`;

    let actionBtnHtml = '';
    if (actionUrl && actionLabel) {
      actionBtnHtml = `
        <div class="mt-2 pt-2 border-top border-light border-opacity-25">
          <a href="${actionUrl}" class="btn btn-sm btn-light text-dark fw-semibold">
            ${actionLabel} &rarr;
          </a>
        </div>
      `;
    }

    let speakIconHtml = '';
    if (sender === 'assistant') {
      speakIconHtml = `
        <button class="btn btn-sm btn-link text-white-50 p-0 ms-2 speak-btn" title="Speak again">
          <i class="bi bi-volume-up"></i>
        </button>
      `;
    }

    const bubbleBg = sender === 'user' ? 'bg-danger text-white' : 'text-white';
    const bubbleStyle = sender === 'user' ? '' : 'background: #543216;';

    msgDiv.innerHTML = `
      <div class="p-3 rounded-4 shadow-sm ${bubbleBg}" style="max-width: 80%; ${bubbleStyle}">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <span class="small fw-bold opacity-75">${sender === 'user' ? 'You' : '🦚 Kalamkari Mitra'}</span>
          ${speakIconHtml}
        </div>
        <div class="message-content" style="white-space: pre-line; line-height: 1.6;">${this.escapeHtml(text)}</div>
        ${actionBtnHtml}
      </div>
    `;

    // Bind speech trigger on speaker icon
    if (sender === 'assistant') {
      const spk = msgDiv.querySelector('.speak-btn');
      if (spk) {
        spk.addEventListener('click', () => {
          this.speakText(text);
        });
      }
    }

    this.chatContainer.appendChild(msgDiv);
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
  }

  appendLoadingMessage() {
    if (!this.chatContainer) return null;
    const loadId = 'loading-' + Date.now();
    const loadDiv = document.createElement('div');
    loadDiv.id = loadId;
    loadDiv.className = 'd-flex mb-3 justify-content-start';
    loadDiv.innerHTML = `
      <div class="p-3 rounded-4 shadow-sm text-white" style="background: #543216; max-width: 80%;">
        <span class="spinner-grow spinner-grow-sm me-2 text-warning" role="status"></span>
        <span class="small">Thinking...</span>
      </div>
    `;
    this.chatContainer.appendChild(loadDiv);
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    return loadId;
  }

  removeLoadingMessage(loadId) {
    if (!loadId) return;
    const el = document.getElementById(loadId);
    if (el) el.remove();
  }

  showAlert(message, type = 'warning') {
    if (!this.alertBox) return;
    if (!message) {
      this.alertBox.style.display = 'none';
      return;
    }
    this.alertBox.className = `alert alert-${type} py-2 px-3 small rounded-3 mb-3`;
    this.alertBox.textContent = message;
    this.alertBox.style.display = 'block';
  }

  escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
}
