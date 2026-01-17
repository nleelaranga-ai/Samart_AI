# 🎓 SamartAI - Bridging the Gap for Rural Students

> **Team Pixel X** | **Track:** AI for Bharat / Public Impact

SamartAI is an omnichannel AI assistant designed to help students in rural India (Tier-2/3) discover government scholarships. It overcomes language barriers and low digital literacy by providing guidance in **local languages (Telugu/English)** via **Telegram (Low Bandwidth)** and **Web**.

## 🚀 Features
* **Omni-channel Access:** Works on Web (Desktop) and Telegram (2G/3G compatible).
* **Multilingual Brain:** Translates queries from Telugu to English, processes them, and replies in Telugu.
* **Zero-UI Interface:** No complex forms; students just chat naturally.
* **Verified Data:** Sourced from *JnanaBhumi* (AP Govt) and *National Scholarship Portal*.

## 🛠️ Tech Stack
* **Brain:** Python, Ollama (Mistral/Llama3), Deep-Translator
* **Interfaces:** Flask (Web), Python-Telegram-Bot (Messaging)
* **Data:** JSON Structure (Scalable to SQL)

## 📸 Screenshots
*(Add screenshots of your Web App and Telegram Chat here)*

## 🏃‍♂️ How to Run
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/yourusername/samart-ai.git](https://github.com/yourusername/samart-ai.git)
    cd samart-ai
    ```
2.  **Install dependencies:**
    ```bash
    pip install flask python-telegram-bot ollama deep-translator
    ```
3.  **Run the System:**
    * **Terminal 1 (Bot):** `python telegram_bot.py`
    * **Terminal 2 (Web):** `python app.py`

## 🔮 Future Scope
* **WhatsApp Integration:** Using Twilio/Meta API for wider reach.
* **Voice Notes:** Integration with OpenAI Whisper for speech-to-text.
* **Document Verification:** OCR to auto-scan caste certificates.
