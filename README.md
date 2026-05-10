# Healthcare Assistant Chatbot

## Project Overview
This project is a web-based Healthcare Assistant Chatbot built as part of an academic project. It provides health-related information and guidance using a Large Language Model (LLM) and Retrieval-Augmented Generation (RAG) tailored for the Indian healthcare context. The system is designed to offer preventive healthcare tips and explain medical terms without diagnosing diseases or prescribing medication.

## Architecture Diagram
```text
+-------------------+        +--------------------+       +-----------------------+
|                   |        |                    |       | Google Colab (GPU)    |
|   Frontend UI     | <----> |   FastAPI Backend  | <---> |                       |
| (HTML/CSS/JS)     |        | (Local Machine)    |       | Ollama (Meditron-7B)  |
|                   |        |                    |       | + Tunnel (ngrok/etc)  |
+-------------------+        +--------------------+       +-----------------------+
                                       ^
                                       |
                                       v
                             +--------------------+
                             | ChromaDB (RAG)     |
                             | Sentence-Transf.   |
                             +--------------------+
```

## Tech Stack
| Component | Technology |
| --- | --- |
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| LLM | Meditron-7B (running via Ollama) |
| RAG & Embeddings | ChromaDB, sentence-transformers (`all-MiniLM-L6-v2`) |
| Deployment/Hosting | Local Backend, Google Colab (Model Hosting) |

## Setup Instructions

### 1. Model Setup (Google Colab)
Since the Meditron-7B model requires significant compute, it is hosted on Google Colab to utilize its free GPU.
1. Open your Google Colab notebook for hosting the model.
2. Run the cells to install Ollama and start the server.
3. Pull and run the `meditron:7b` model.
4. Run the cell to expose the Ollama server via a tunnel (e.g., ngrok or Cloudflare).
5. Copy the generated public URL.

### 2. Local Backend Setup
1. Clone the repository and navigate to the `backend` directory.
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the backend directory (see Environment Variables below).
5. Load the healthcare documents into the vector database:
   ```bash
   python load_rag_data.py
   ```
6. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### 3. Frontend Setup
1. Open the `frontend/index.html` file in any modern web browser.
2. The UI will automatically connect to the backend running at `http://localhost:8000`.

## Environment Variables
Create a `.env` file in the `backend/` directory with the following variables:

| Variable | Description | Example |
| --- | --- | --- |
| `LLM_PROVIDER` | The LLM provider to use | `ollama` |
| `OLLAMA_BASE_URL` | The public URL of the Colab tunnel | `https://<your-tunnel-url>` |
| `OLLAMA_MODEL` | The model to use | `meditron:7b` |
| `ENABLE_RAG` | Whether to enable RAG functionality | `true` |

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/chat` | POST | Main endpoint for chat interactions. Accepts a message and returns the bot's response. |
| `/health` | GET | Health check endpoint to verify backend status. |
| `/disclaimer` | GET | Returns the standard medical disclaimer used by the system. |

## How the Colab Tunnel Works
To bypass the need for a local GPU, the heavy Meditron-7B LLM runs on Google Colab's infrastructure. Since Colab instances are isolated, a tunneling service (like ngrok, Cloudflare Tunnel, or Colab's built-in tunneling) is used to expose the local Ollama port (11434) to the public internet. The local FastAPI backend uses this public URL to send API requests to the model seamlessly as if it were running locally.

## Screenshots
*(Add screenshots of the web interface here)*
- [Screenshot 1: Chat Interface Placeholder]
- [Screenshot 2: RAG Context Example Placeholder]
- [Screenshot 3: Emergency Warning Placeholder]

## Medical Disclaimer
**The information provided by this chatbot is for educational and informational purposes only.** It does NOT diagnose diseases, prescribe medication, or replace professional medical advice. Always consult a qualified healthcare provider for any medical concerns. In case of a medical emergency, please call your local emergency services (e.g., 108 in India) immediately.

## Academic Context
This project was developed as part of an academic assignment for the "Emerging Tools and Technologies" course. Safety and correctness are prioritized over feature richness.
