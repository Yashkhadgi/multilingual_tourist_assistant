<div align="center">

# 🧳 BhashaYatra (भाषा यात्रा)
### Multilingual Agentic AI Tourist Assistant for India

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestrator-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Anthropic Claude](https://img.shields.io/badge/LLM-Anthropic%20Claude-8A2BE2.svg)](https://anthropic.com)
[![Sarvam AI](https://img.shields.io/badge/Voice%20%26%20Indic%20AI-Sarvam%20AI-00C49F.svg)](https://www.sarvam.ai/)
[![ChromaDB](https://img.shields.io/badge/Vector%20Store-ChromaDB-red.svg)](https://www.trychroma.com/)
[![Gradio](https://img.shields.io/badge/UI-Gradio%204-FF7C00.svg?logo=gradio&logoColor=white)](https://gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<p align="center">
  <b>A state-of-the-art, multi-agent AI tourist companion offering localized travel planning, voice-first Indic language conversations, real-time safety response, and cultural etiquette guidance.</b>
</p>

</div>

---

## 🌟 Overview

Traveling across India presents incredible diversity—from languages and cultural customs to navigation nuances and local safety practices. **BhashaYatra (भाषा यात्रा)** is an open-source, agentic AI tourist assistant designed to bridge language barriers, deliver grounded itineraries, and provide context-aware assistance at every stage of the journey.

Powered by a **LangGraph-driven orchestrator**, BhashaYatra routes user queries to specialized autonomous agents equipped with live tools:

- 🗺️ **Itinerary & Route Planner** with real-time Google Maps data, OpenWeather forecasts, and live Tavily web-grounded distance verification.
- 🏛️ **Local Knowledge RAG Agent** powered by ChromaDB vector search over curated historical, cultural, and destination data.
- 🚨 **Emergency & Safety Agent** providing instant nearest hospital/police station lookup and translated distress phrases.
- 🛕 **Cultural Etiquette Agent** offering guidance on temple dress codes, tipping, photography norms, and local customs.
- 🎙️ **Multilingual Voice Assistant** with full Speech-to-Text (STT) and Text-to-Speech (TTS) support for 8+ Indic languages via Sarvam AI.
- 💱 **Live Currency Converter** supporting multiple global currencies against INR.

---

## 🏗️ System Architecture

BhashaYatra utilizes a modular, graph-based agent architecture where a centralized orchestrator classifies intents and conditionally delegates tasks to domain-specific worker agents.

```mermaid
flowchart TD
    User([👤 User / Tourist]) --> UI[🖥️ Gradio UI / Voice Interface]
    
    UI --> STT[🎙️ Sarvam STT (saaras:v3)]
    STT --> ORCH[🧭 LangGraph Orchestrator Node]
    UI -- Text Input --> ORCH
    
    ORCH --> MEM[(💾 SQLite Session Memory)]
    
    ORCH -->|Intent: 'planner'| PLAN[🗺️ Planner Agent]
    ORCH -->|Intent: 'info'| RAG[🏛️ Local Info / RAG Agent]
    ORCH -->|Intent: 'safety'| SAFE[🚨 Emergency / Safety Agent]
    ORCH -->|Intent: 'etiquette'| ETIQ[🛕 Cultural Etiquette Agent]
    
    PLAN --> T_MAPS[📍 Google Maps API]
    PLAN --> T_WEATH[🌤️ OpenWeather API]
    PLAN --> T_SEARCH[🔍 Tavily Web Search]
    
    RAG --> V_CHROMA[(⚡ ChromaDB Vector Store)]
    
    SAFE --> T_MAPS2[🏥 Nearby Hospitals / Police]
    SAFE --> T_TRANS[🌐 Sarvam Translate]
    
    PLAN --> RESP[📝 Agent Response Synthesis]
    RAG --> RESP
    SAFE --> RESP
    ETIQ --> RESP
    
    RESP --> TTS[🔊 Sarvam TTS (bulbul:v3)]
    RESP --> UI
    TTS --> UI
```

---

## 🤖 Specialized Multi-Agent Team

| Agent | Responsibility | Tools & Integrations | LLM Engine |
|---|---|---|---|
| **🧭 Orchestrator** | Dynamic intent classification & conditional routing | LangGraph, Prompt Taxonomy | Claude 3.5 / 3.7 Sonnet |
| **🗺️ Planner Agent** | Day-wise itineraries, route planning, transport estimates | Google Maps, OpenWeather, Tavily Search | Claude 3.5 / 3.7 Sonnet |
| **🏛️ Local Info (RAG)** | Facts about monuments, operating hours, history, ticket info | ChromaDB Vector Store | Claude 3.5 Haiku |
| **🚨 Safety Agent** | Emergency hotlines (112/100/108), nearest medical/police aid, distress translations | Google Maps Places, Sarvam Translate | Claude 3.5 Haiku |
| **🛕 Etiquette Agent** | Temple dress codes, footwear rules, tipping norms, social customs | Cultural Knowledge Base | Claude 3.5 Haiku |

---

## 🌐 Supported Indic Languages (Voice & Text)

BhashaYatra natively supports bidirectional speech and text across major Indic languages:

| Language | Code | STT Support | TTS Voice Synthesis |
|---|---|---|---|
| **Hindi (हिन्दी)** | `hi-IN` | ✅ Full | ✅ Multi-speaker (Advait/Ritu/etc.) |
| **English (Indian)** | `en-IN` | ✅ Full | ✅ Natural accent |
| **Bengali (বাংলা)** | `bn-IN` | ✅ Full | ✅ Regional voice |
| **Tamil (தமிழ்)** | `ta-IN` | ✅ Full | ✅ Regional voice |
| **Telugu (తెలుగు)** | `te-IN` | ✅ Full | ✅ Regional voice |
| **Marathi (मराठी)** | `mr-IN` | ✅ Full | ✅ Regional voice |
| **Gujarati (ગુજરાતી)** | `gu-IN` | ✅ Full | ✅ Regional voice |
| **Kannada (ಕನ್ನಡ)** | `kn-IN` | ✅ Full | ✅ Regional voice |

---

## 📂 Project Structure

```text
multilingual-tourist-agent/
├── agents/                     # Specialized agent implementations
│   ├── orchestrator_graph.py   # LangGraph state machine & router
│   ├── orchestrator.py         # Orchestrator core
│   ├── planner_agent.py        # Itinerary & travel planning agent
│   ├── rag_agent.py            # Local knowledge & RAG agent
│   ├── safety_agent.py         # Emergency & medical/police assistance
│   └── etiquette_agent.py      # Cultural norms & etiquette guidance
├── config/                     # Configuration and environment settings
│   ├── .env.example            # Template for environment variables
│   └── settings.py             # App-wide settings & key validation
├── data/                       # Datasets and vector store
│   ├── embeddings/             # Persistent ChromaDB vector index
│   └── knowledge_base/         # Curated destination knowledge base (destinations.json)
├── memory/                     # Conversation persistence
│   ├── session_memory.py       # SQLite sliding-window session store
│   └── sessions.db             # Local SQLite database
├── scripts/                    # Utilities and build scripts
│   └── build_knowledge_base.py # Ingestion script for ChromaDB
├── tools/                      # External API wrappers and utilities
│   ├── currency_tool.py        # Exchange rate converter
│   ├── llm_wrapper.py          # Anthropic Claude API client
│   ├── maps_tool.py            # Google Maps Geocoding & Places
│   ├── translation_tool.py     # Sarvam text translation
│   ├── voice_tool.py           # Sarvam STT & TTS pipeline
│   ├── weather_tool.py         # OpenWeather 3-day forecast
│   └── web_search_tool.py      # Tavily search for live verification
├── ui/                         # Frontend user interface
│   └── app.py                  # Gradio web interface (Chat + Voice)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🔑 Environment Configuration

Create a `.env` file in the `config/` directory (or root) based on `config/.env.example`:

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | **Yes** | Anthropic API key for Claude models |
| `ORCHESTRATOR_MODEL` | No | Model for orchestrator (Default: `claude-sonnet-4-5`) |
| `PLANNER_MODEL` | No | Model for itinerary planning (Default: `claude-sonnet-4-5`) |
| `RAG_MODEL` | No | Model for local info (Default: `claude-haiku-4-5`) |
| `SAFETY_MODEL` | No | Model for safety responses (Default: `claude-haiku-4-5`) |
| `ETIQUETTE_MODEL` | No | Model for cultural guidance (Default: `claude-haiku-4-5`) |
| `SARVAM_API_KEY` | Optional | For Indic STT, TTS, and translation |
| `GOOGLE_MAPS_API_KEY` | Optional | For live attractions, distances, and nearby emergency places |
| `OPENWEATHER_API_KEY` | Optional | For real-time 3-day weather forecasts |
| `EXCHANGE_RATE_API_KEY` | Optional | For live currency conversion |
| `TAVILY_API_KEY` | Optional | For live web search and route distance verification |

---

## 🚀 How to Run (Step-by-Step Guide)

Follow these instructions to set up and run BhashaYatra locally on your machine.

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- An **Anthropic API key** (Claude).
- *(Optional but recommended)* API keys for **Sarvam AI**, **Google Maps**, **OpenWeatherMap**, **ExchangeRate-API**, and **Tavily**.

---

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/multilingual-tourist-agent.git
cd multilingual-tourist-agent
```

---

### 3. Create and Activate a Virtual Environment

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

---

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 5. Set Up Environment Variables
Copy the example environment file and fill in your API keys:
```bash
cp config/.env.example config/.env
```
Edit `config/.env` in your preferred text editor:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SARVAM_API_KEY=your_sarvam_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

### 6. Ingest the Local Knowledge Base (ChromaDB)
Initialize and index the local destination knowledge base into ChromaDB:
```bash
python scripts/build_knowledge_base.py
```
*Output: `Ingested X documents into ChromaDB collection 'tourist_kb'.`*

---

### 7. Launch the Application
Start the Gradio web interface:
```bash
python ui/app.py
```

Once running, open your browser and navigate to:
```text
http://localhost:7860
```

---

### 8. Testing Individual Agents (CLI)
You can also run and test individual agents directly from the command line:

- **Test Planner Agent**:
  ```bash
  python agents/planner_agent.py
  ```
- **Test Local Info / RAG Agent**:
  ```bash
  python agents/rag_agent.py
  ```
- **Test Safety & Emergency Agent**:
  ```bash
  python agents/safety_agent.py
  ```
- **Test Cultural Etiquette Agent**:
  ```bash
  python agents/etiquette_agent.py
  ```
- **Test Currency Converter Tool**:
  ```bash
  python tools/currency_tool.py
  ```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve BhashaYatra:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome-feature`).
3. Commit your changes (`git commit -m 'Add awesome feature'`).
4. Push to the branch (`git push origin feature/awesome-feature`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ for travelers exploring the incredible culture and heritage of India.</sub>
</div>
