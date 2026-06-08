# Simple LLM Docker

REST API sederhana yang menggunakan LangChain + OpenAI GPT-4o-mini, dibungkus dengan FastAPI dan siap di-deploy via Docker.

## Struktur Project

```
simple-llm-docker/
├── main.py           # FastAPI app + LangChain logic
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker image definition
├── .dockerignore     # File yang dikecualikan dari Docker build
├── .env              # API key (jangan di-commit ke git)
└── README.md
```

## Endpoint

### `POST /chat`

Mengirim pertanyaan beserta history percakapan, mendapatkan jawaban dari LLM.

**Request Body:**
```json
{
  "question": "Siapa presiden Indonesia?",
  "history": "User: Halo\nAssistant: Halo! Ada yang bisa saya bantu?"
}
```

**Response:**
```json
{
  "answer": "Presiden Indonesia saat ini adalah ...",
  "token_input": 85,
  "token_output": 42
}
```

| Field          | Tipe   | Keterangan                        |
|----------------|--------|-----------------------------------|
| `question`     | string | Pertanyaan dari user              |
| `history`      | string | History percakapan (boleh kosong) |
| `answer`       | string | Jawaban dari LLM                  |
| `token_input`  | int    | Jumlah token yang digunakan input |
| `token_output` | int    | Jumlah token yang dihasilkan      |

### `GET /health`

Health check endpoint.

```json
{ "status": "ok" }
```

---

## Cara Menjalankan

### 1. Lokal (tanpa Docker)

**Prasyarat:** Python 3.11+

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Dengan Docker

**Build image:**
```bash
docker build -t simple-llm-docker .
```

**Run container** (inject `.env` ke container):
```bash
docker run -p 8000:8000 --env-file .env simple-llm-docker
```

API tersedia di `http://localhost:8000`.

Dokumentasi interaktif (Swagger UI) tersedia di `http://localhost:8000/docs`.

---

## Konfigurasi

Buat file `.env` di root project:

```env
OPENAI_API_KEY=sk-...
```

> **Penting:** Jangan commit file `.env` ke repository. Tambahkan ke `.gitignore`.
