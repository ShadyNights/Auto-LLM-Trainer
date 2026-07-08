# Traveler LLM

Traveler LLM is a production-grade AI Travel Planner powered by a **Continuous Feedback Learning Pipeline**.   

Unlike simple wrapper applications, Traveler LLM features an event-driven architecture that automatically captures user feedback, evaluates generated itineraries, and queues high-quality interactions to evolve its dataset and inference configurations.

> **Note**: This architecture is designed to build datasets and promote inference configurations (prompts and provider settings). While it does not automatically retrain foundation model weights today, the pipeline exposes a clean pluggable interface for future LoRA/SFT trainer integration.

## Architecture Highlights
- **Single Source of Truth**: PostgreSQL handles all operational data, state, events, and background queues.
- **Repository Pattern**: Strict decoupling of SQL queries from business logic.
- **Provider Abstraction**: A unified `ProviderInterface` currently supporting Groq, designed for trivial expansion to OpenAI or Gemini.
- **Continuous Feedback Learning Pipeline**: Independent stages (`Collect`, `Dataset`, `Evaluate`, `Promote`, `Cleanup`) that asynchronously process the `training_queue`.
- **Operational Readiness**: Structured JSON logging, Domain-Specific Exceptions, Dead Letter Queues (DLQ), and Health Checks.

---

## Installation & Deployment

We strongly recommend deploying Traveler LLM via Docker Compose, which seamlessly orchestrates the Streamlit application and the PostgreSQL database.

### Prerequisites
- Docker and Docker Compose
- A [Groq API Key](https://console.groq.com/)

### 1. Configure Environment
Clone the repository and set up your secure environment variables:
```bash
cp .env.example .env
```
Edit `.env` and insert your `GROQ_API_KEY`. Be sure to set secure passwords for your database user!

### 2. Build and Start
Run the following command to build the Docker image and start the cluster:
```bash
docker-compose up -d --build
```
The application will wait for PostgreSQL to become healthy before booting. 

### 3. Initialize the Database Schema
Once the containers are running, execute the database migrations to set up the tables:
```bash
docker-compose exec app python setup_database.py
```

### 4. Access the Application
Navigate to `http://localhost:8501` in your browser.

---

## Background Jobs (The Pipeline)

The Continuous Feedback Learning Pipeline runs independently of the web application. You can execute it via the CLI:
```bash
# Run the complete end-to-end pipeline:
docker-compose exec app python background_jobs.py pipeline

# Or run specific independent stages:
docker-compose exec app python background_jobs.py train
docker-compose exec app python background_jobs.py evaluate
docker-compose exec app python background_jobs.py promote
```

---

## Troubleshooting

- **Database Connection Failed**: Ensure `docker-compose up` was successful and the `db` service is healthy. Verify the credentials in your `.env` match the compose file variables.
- **ProviderUnavailable / GROQ_API_KEY error**: Verify your API key is correctly injected into the container via `.env`.
- **PromptNotFound**: Ensure the `prompts/travel/v1.md` file exists and has not been modified without updating the `prompts_metadata` checksum in the database.
- **Queue tasks stuck**: If a task fails 5 times, it enters the Dead Letter Queue (`status = 'dead'`). Check the structured JSON logs in `docker-compose logs app` for the exact Python exception.
