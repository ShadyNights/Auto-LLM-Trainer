# Deployment Guide

## Prerequisites
- PostgreSQL 14+
- Python 3.10+
- Groq API Key

## 1. Environment Configuration
Copy `.env.example` to `.env` and populate your secrets.
```bash
cp .env.example .env
# Edit .env to include your GROQ_API_KEY and secure PostgreSQL credentials.
```

## 2. Database Initialization
Ensure PostgreSQL is running and your `PGUSER` has the correct privileges.
Apply the schema migrations:
```bash
python setup_database.py
```
*(This script executes all files in `migrations/` sequentially).*

## 3. Application Startup
Start the Streamlit UI:
```bash
streamlit run app.py
```
The application will perform startup validations. If critical checks fail (e.g., DB unreachable, missing API key), the app will halt.

## 4. Background Jobs
To run the Continuous Feedback Learning Pipeline, schedule the CLI via Cron, SystemD, or a CI/CD pipeline:
```bash
# Run the full pipeline
python background_jobs.py pipeline

# Or run individual stages
python background_jobs.py train
python background_jobs.py evaluate
python background_jobs.py promote
```
