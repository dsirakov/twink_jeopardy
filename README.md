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

This will:
- Build the FastAPI application image
- Start PostgreSQL database on port 5432
- Start the API server on http://localhost:8000
- Enable hot-reload for development

3. **Load the dataset** (in a new terminal):

```bash
docker-compose exec api python scripts/load_dataset.py
```

4. **Access the API**:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Useful Docker Commands

```bash
# Start containers in the background
docker-compose up -d

# View logs from all services
docker-compose logs -f

# View logs from specific service
docker-compose logs -f api
docker-compose logs -f db

# Stop containers
docker-compose down

# Remove all data and volumes
docker-compose down -v

# Access the database shell
docker-compose exec db psql -U postgres -d jeopardy

# Run a command in the API container
docker-compose exec api python scripts/load_dataset.py

# Restart services
docker-compose restart
```

### Docker Architecture

- **db**: PostgreSQL 15-alpine with persistent volume storage
- **api**: Python 3.11-slim FastAPI application with live code reloading

Both services communicate via a dedicated Docker network. The API depends on the database health check before starting.

## API Endpoints

### Get a Random Question

```http
GET /question?round=Jeopardy!&value=200
```

**Parameters:**
- `round` (string): Question round (e.g., "Jeopardy!", "Double Jeopardy!")
- `value` (integer): Question value in dollars (e.g., 200, 400, 600, 800, 1000)

**Response:**
```json
{
  "question_id": 1,
  "round": "Jeopardy!",
  "category": "SCIENCE",
  "value": "$200",
  "question": "What is photosynthesis?"
}
```

### Verify an Answer

```http
POST /verify-answer
Content-Type: application/json

{
  "question_id": 1,
  "user_answer": "photosynthesis"
}
```

**Request Body:**
- `question_id` (integer): ID of the question to verify
- `user_answer` (string): User's answer to verify

**Response:**
```json
{
  "is_correct": true,
  "ai_response": "Correct! Photosynthesis is the process by which plants convert light energy into chemical energy stored in glucose molecules..."
}
```

## Answer Verification Logic

The API uses a three-tier verification system:

1. **Exact Match** - Normalized string comparison (removes case and special characters)
2. **Fuzzy Matching** - Tolerates typos with >80% string similarity
3. **Semantic Similarity** - Uses OpenAI embeddings with >75% cosine similarity threshold

## Project Structure

```
twink_jeopardy/
├── app/
│   ├── main.py              # FastAPI application setup
│   ├── config.py            # Configuration and settings
│   ├── api/
│   │   ├── questions.py     # Question retrieval endpoint
│   │   └── verify.py        # Answer verification endpoint
│   ├── db/
│   │   ├── models.py        # SQLAlchemy ORM models
│   │   └── session.py       # Database session management
│   └── services/
│       ├── llm_client.py    # OpenAI client singleton
│       └── verifier.py      # Answer verification logic
├── scripts/
│   └── load_dataset.py      # Dataset loading script
├── data/
│   └── JEOPARDY_CSV.csv     # Jeopardy questions dataset
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technology Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI**: OpenAI API (embeddings & GPT-4o-mini)
- **Configuration**: Pydantic Settings
- **Testing**: pytest

## Requirements

See [requirements.txt](requirements.txt) for the complete list of dependencies:

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- pydantic-settings
- pytest
- openai>=1.0.0

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and your `DATABASE_URL` in `.env` is correct.

### OpenAI API Error

Verify that your `OPENAI_API_KEY` is valid and has sufficient credits.

### No Questions Found

Run `python scripts/load_dataset.py` to load the Jeopardy dataset into the database.

## License

MIT
