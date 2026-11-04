# 🤝 FinSaathi — AI Agent for Digital Financial Literacy

> **Problem Statement #7** — An AI Agent powered by **IBM Granite (watsonx.ai)** and **RAG (Retrieval-Augmented Generation)** that helps users understand and safely navigate digital financial tools and practices.

[![IBM Granite](https://img.shields.io/badge/IBM-Granite%20LLM-0f62fe?logo=ibm)](https://www.ibm.com/watsonx)
[![watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-009d9a)](https://www.ibm.com/watsonx)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python)](https://python.org)

---

## 📌 Overview

**FinSaathi** is a multilingual, RAG-powered AI assistant that empowers Indian citizens with financial literacy knowledge. Built on **IBM Granite** via **IBM Cloud Lite / watsonx.ai**, it retrieves reliable, curated content from government portals (RBI, NPCI, SEBI, IRDAI) and answers questions in the user's preferred language.

### 💡 What it can do
| Topic | Example Question |
|---|---|
| 💳 UPI & Digital Payments | "How do I send money via UPI?" |
| 🛡️ Scam Prevention | "What are common UPI scams?" |
| 📊 Interest Rates | "What is a safe interest rate for a loan?" |
| 💰 Budgeting | "How do I create a monthly budget?" |
| 📈 Investments | "What are good options for beginners?" |
| 💳 Credit Score | "How do I improve my CIBIL score?" |
| 🏛️ Govt Schemes | "What is Jan Dhan Yojana?" |
| 🛡️ Insurance | "What insurance should I buy first?" |

### 🌐 Multilingual Support
Supports **11 Indian languages + more**: English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu — auto-detected from user input.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   FinSaathi System Architecture                  │
├─────────────────────────────────────────────────────────────────┤
│  User (any language)                                             │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────────────────────────────────────────┐           │
│  │         FastAPI Backend (main.py)                │           │
│  │   POST /chat  GET /health  GET /topics           │           │
│  └────────────────────┬─────────────────────────────┘           │
│                       │                                          │
│       ┌───────────────┼────────────────────┐                    │
│       ▼               ▼                    ▼                     │
│  ┌─────────┐   ┌────────────┐    ┌──────────────────┐           │
│  │  i18n   │   │  RAG       │    │  IBM Granite LLM │           │
│  │Translator│   │ Pipeline   │    │  (watsonx.ai)    │           │
│  │         │   │            │    │                  │           │
│  │ IBM WT  │   │ ChromaDB   │    │ granite-13b-     │           │
│  │ Google  │   │ Vector     │    │ instruct-v2      │           │
│  │ Fallback│   │ Store      │    │                  │           │
│  └─────────┘   └────────────┘    └──────────────────┘           │
│                       │                                          │
│               ┌───────┴────────┐                                 │
│               │ Knowledge Base │                                 │
│               │ (12 curated    │                                 │
│               │  documents)    │                                 │
│               │ RBI·NPCI·SEBI  │                                 │
│               │ IRDAI·Govt     │                                 │
│               └────────────────┘                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Technology | Purpose |
|---|---|---|
| **LLM** | IBM Granite 13B Instruct v2 | Answer generation |
| **RAG Retriever** | ChromaDB + sentence-transformers | Semantic search |
| **Embeddings** | paraphrase-multilingual-MiniLM-L12-v2 | Multilingual vectors |
| **Translation** | IBM Watson Translator / deep-translator | Multilingual I/O |
| **Lang Detection** | langdetect | Auto-detect user language |
| **Backend** | FastAPI + uvicorn | REST API |
| **Frontend** | Vanilla HTML/CSS/JS | Chat UI |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- IBM Cloud account (Lite tier is sufficient)
- IBM watsonx.ai project

### 1. Clone the repository
```bash
git clone https://github.com/your-org/digital-financial-ai-agent.git
cd digital-financial-ai-agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure IBM credentials
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

Edit `.env`:
```env
IBM_WATSONX_API_KEY=your_actual_ibm_cloud_api_key
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
IBM_WATSONX_PROJECT_ID=your_watsonx_project_id
IBM_GRANITE_MODEL_ID=ibm/granite-13b-instruct-v2
```

> **Where to get credentials:**
> 1. Go to [IBM Cloud Console](https://cloud.ibm.com)
> 2. Create a **watsonx.ai** service instance (Lite tier is free)
> 3. Create a project in [watsonx.ai Studio](https://dataplatform.cloud.ibm.com)
> 4. Generate an API key under **Manage → Access (IAM) → API keys**

### 5. Ingest the knowledge base
```bash
python scripts/ingest.py
```
This embeds all financial documents into ChromaDB. Takes ~2 minutes on first run.

### 6. Run the server
```bash
python main.py
```
Or with uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Open the UI
Navigate to **http://localhost:8000** in your browser.

API docs available at **http://localhost:8000/docs** (Swagger UI).

---

## 📁 Project Structure

```
digital-financial-ai-agent/
├── .env                          # 🔑 Your credentials (not committed)
├── .env.example                  # Template for .env
├── main.py                       # FastAPI application entry point
├── requirements.txt              # Python dependencies
│
├── app/
│   ├── core/
│   │   ├── config.py             # Settings loaded from .env
│   │   └── logging.py            # Logging setup
│   │
│   ├── rag/
│   │   ├── knowledge_base.py     # 12 curated financial literacy docs
│   │   ├── embeddings.py         # Multilingual sentence-transformer
│   │   └── vectorstore.py        # ChromaDB ingestion & retrieval
│   │
│   ├── agent/
│   │   ├── granite_llm.py        # IBM Granite LangChain wrapper
│   │   ├── prompts.py            # RAG prompt templates
│   │   └── rag_chain.py          # Full RAG pipeline orchestration
│   │
│   ├── api/
│   │   ├── models.py             # Pydantic request/response schemas
│   │   └── routes.py             # FastAPI endpoints
│   │
│   └── i18n/
│       └── translator.py         # Multilingual translation layer
│
├── frontend/
│   └── index.html                # Chat UI (IBM Carbon Design inspired)
│
├── data/
│   ├── documents/                # (Add custom PDF/TXT docs here)
│   └── vectorstore/              # ChromaDB persisted data
│
├── scripts/
│   ├── ingest.py                 # Knowledge base ingestion script
│   └── test_granite.py           # IBM Granite connectivity test
│
└── tests/
    ├── test_api.py               # FastAPI endpoint tests
    └── test_rag.py               # RAG pipeline unit tests
```

---

## 🔌 API Reference

### `POST /chat`
Main chat endpoint.

**Request:**
```json
{
  "message": "How do I send money via UPI?",
  "history": [
    {"role": "user", "content": "What is UPI?"},
    {"role": "assistant", "content": "UPI stands for Unified Payments Interface..."}
  ],
  "language": "hi",
  "category": "upi"
}
```

**Response:**
```json
{
  "answer": "UPI से पैसे भेजने के लिए...",
  "sources": [
    {"title": "How to Send Money via UPI", "category": "upi", "source": "NPCI"}
  ],
  "detected_language": "hi",
  "english_query": "How do I send money via UPI?"
}
```

### `GET /health`
Returns service health, vector store status, and supported languages.

### `GET /topics`
Returns quick-access financial topics with sample queries for the UI.

### `GET /languages`
Returns all supported languages with their display names.

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only API tests
pytest tests/test_api.py -v

# Run only RAG tests
pytest tests/test_rag.py -v
```

---

## 🌐 Multilingual Flow

```
User asks in Hindi: "UPI से पैसे कैसे भेजें?"
         │
         ▼
    langdetect → "hi"
         │
         ▼
  IBM Watson / deep-translator → "How to send money via UPI?" (English)
         │
         ▼
    ChromaDB semantic search (multilingual embeddings)
         │
         ▼
    IBM Granite generates answer in English
         │
         ▼
  IBM Watson / deep-translator → Answer in Hindi
         │
         ▼
  "UPI से पैसे भेजने के लिए: BHIM, PhonePe या Google Pay खोलें..."
```

---

## 🔒 Security & Privacy

- No user data is stored or logged beyond the current session.
- API keys are stored only in the `.env` file (never committed to git).
- The `.gitignore` excludes `.env`, `data/vectorstore/`, and `__pycache__`.
- Rate limiting is configurable via `.env` (default: 20 req/min).

---

## 📚 Knowledge Sources

| Source | Topics Covered |
|---|---|
| [RBI](https://www.rbi.org.in) | Interest rates, banking, consumer protection |
| [NPCI / BHIM](https://www.npci.org.in) | UPI, digital payments |
| [SEBI](https://www.sebi.gov.in) | Investments, mutual funds |
| [IRDAI](https://www.irdai.gov.in) | Insurance |
| [Income Tax Dept](https://incometax.gov.in) | Tax basics |
| [Cyber Dost / MHA](https://cybercrime.gov.in) | Fraud prevention |
| [India.gov.in](https://www.india.gov.in) | Government schemes |

---

## 🛠️ Technologies Used

| Category | Technology |
|---|---|
| **LLM** | IBM Granite 13B Instruct v2 (watsonx.ai) |
| **Cloud** | IBM Cloud Lite |
| **RAG Framework** | LangChain 0.2 |
| **Vector Store** | ChromaDB |
| **Embeddings** | paraphrase-multilingual-MiniLM-L12-v2 |
| **Translation** | IBM Watson Language Translator |
| **Backend** | FastAPI + Uvicorn |
| **Config** | Pydantic-settings |
| **Testing** | Pytest |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-topic`
3. Add your knowledge documents in `app/rag/knowledge_base.py`
4. Run tests: `pytest tests/ -v`
5. Submit a pull request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built for IBM Internship Project — Problem Statement #7: AI Agent for Digital Financial Literacy*  
*Powered by IBM Granite on watsonx.ai (IBM Cloud Lite)*
