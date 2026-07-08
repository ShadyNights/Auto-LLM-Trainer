# Deployment Guide

> [!TIP]
> Traveler LLM is designed for secure, container-friendly deployment. This guide covers standard environment setup for production execution.

---

## Prerequisites
- **PostgreSQL**: Version 14 or higher.
- **Python**: Version 3.10 or higher.
- **Groq API Key**: For LLM inference capabilities.

---

## 1. Environment Initialization

Strict configuration via environment variables ensures no hardcoded secrets exist in the codebase.

```bash
# 1. Duplicate the template
cp .env.example .env

# 2. Populate credentials
# Edit .env to inject your GROQ_API_KEY and PostgreSQL connection string.
```

## 2. Infrastructure Setup

Initialize the unified PostgreSQL schema. The database user must have standard `CREATE` and `GRANT` privileges for the initial run.

```bash
# Execute the unified initialization script
python setup_database.py
```
*Note: This strictly executes `migrations/001_initial_schema.sql`, constructing all tables, views, and seed data in a single transaction.*

## 3. Application Execution

Launch the native UI. The application will automatically execute startup integrity checks against the database and environment variables.

```bash
streamlit run app.py
```

> [!WARNING]  
> If critical dependencies (e.g., Database unreachable, Provider Key missing) are invalid, the application will proactively halt with a distinct error message rather than degrading silently.

## 4. Background Pipeline Execution

To activate the Continuous Feedback Learning Pipeline, schedule the orchestration script via SystemD, Cron, or a dedicated container worker.

```bash
# Execute the complete learning lifecycle
python background_jobs.py pipeline

# Execute modular stages independently
python background_jobs.py train
python background_jobs.py evaluate
python background_jobs.py promote
```
