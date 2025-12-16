# Twink Jeopardy API

A FastAPI-based Jeopardy question service with AI-powered answer verification and feedback using OpenAI.

## Features

- 🎯 Random Jeopardy question retrieval by round and value
- ✅ Multi-layered answer verification (exact match, fuzzy matching, semantic similarity)
- 🤖 AI-generated feedback on user answers using GPT-4o-mini
- 📊 PostgreSQL database with CSV data loading
- 🔒 Environment-based configuration with `.env` support

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- OpenAI API key

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd twink_jeopardy
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and configure it with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/jeopardy
OPENAI_API_KEY=your-openai-api-key-here
```

### 5. Load the Dataset

```bash
python scripts/load_dataset.py
```

This will load Jeopardy questions from `data/JEOPARDY_CSV.csv` into the PostgreSQL database.

## Running the API

### Development Mode (Local)

Start the API server with hot-reload enabled:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Access the Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Running with Docker

### Prerequisites for Docker

- Docker
- Docker Compose

### Quick Start

1. **Set your OpenAI API key** (optional if using `.env`):

```bash
export OPENAI_API_KEY=your-openai-api-key-here
```

Or add it to your `.env` file:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

2. **Start the services**:

```bash
docker-compose up --build
```

3. **Load the dataset** (in a new terminal):

```bash
docker-compose exec api python scripts/load_dataset.py
```

4. **Access the API**:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Answer Verification Logic

The API uses a three-tier verification system:

1. **Exact Match** - Normalized string comparison (removes case and special characters)
2. **Fuzzy Matching** - Tolerates typos with >80% string similarity
3. **Semantic Similarity** - Uses OpenAI embeddings with >75% cosine similarity threshold
