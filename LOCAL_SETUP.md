# Local Development Setup Guide

> [!NOTE]
> Welcome to the Traveler LLM project! This guide provides a comprehensive, step-by-step walkthrough to get the application running successfully on your local Windows/macOS/Linux machine.

---

## 1. Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.10+**: Make sure Python is added to your system PATH.
- **PostgreSQL 14+**: A local database server running on the default port (`5432`).
- **Git**: For version control.
- **Groq API Key**: You need an active API key from the [Groq Console](https://console.groq.com/).

---

## 2. Environment Configuration

### Clone the Repository
Open your terminal and clone the repository:
```bash
git clone https://github.com/your-org/traveler-llm.git
cd "traveler-llm"
```

### Create a Virtual Environment
It is strictly recommended to isolate your dependencies using a Python virtual environment.

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
With the virtual environment activated, install the required packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> [!WARNING]  
> **PostgreSQL Dependency Note (psycopg2)**
> We utilize `psycopg2-binary` to avoid requiring C-compilers on local setups. If you encounter a `No module named 'psycopg2'` error during execution, ensure your virtual environment is activated and the `requirements.txt` installation completed successfully.

---

## 3. Database Initialization

### Create the Database and User
Open your PostgreSQL terminal (e.g., `psql -U postgres`) or use a GUI tool like pgAdmin or DBeaver to create the database and a dedicated local user.

```sql
CREATE DATABASE traveler_db;
CREATE USER traveler_app_user WITH PASSWORD 'local_password_123';
GRANT ALL PRIVILEGES ON DATABASE traveler_db TO traveler_app_user;
```

### Configure the Environment Variables
Duplicate the example environment file:
```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```
Edit `.env` to include your credentials:
```ini
GROQ_API_KEY="gsk_your_groq_api_key_here"
DB_NAME="traveler_db"
DB_USER="traveler_app_user"
DB_PASSWORD="local_password_123"
DB_HOST="localhost"
DB_PORT="5432"
```

### Execute the Unified Schema Migration
Initialize the application tables, seed data, and initial state by running the unified setup script. This script executes `migrations/001_initial_schema.sql`.

```bash
python setup_database.py
```
*You should see output confirming that the database initialization was successful.*

---

## 4. Running the Application

Traveler LLM is split into two primary components: the UI and the Background Pipeline.

### Launch the Streamlit UI
Start the web interface. This will open the application in your default web browser (typically at `http://localhost:8501`).
```bash
streamlit run app.py
```

### Run the Background Learning Pipeline
The background queue processes user feedback, generates datasets, and evaluates models asynchronously. Open a **second terminal window**, activate your virtual environment, and run:

```bash
# Run the complete pipeline execution
python background_jobs.py pipeline
```

---

## 5. Troubleshooting

> [!TIP]
> **Common Issues:**
> - **Database Connection Refused**: Verify that your local PostgreSQL service is actually running and that the port/password in `.env` matches your configuration.
> - **Module Not Found**: Ensure you have activated your virtual environment (`.\venv\Scripts\Activate.ps1`) before executing `python` commands.
> - **Missing API Key**: If the UI immediately halts with a configuration error, ensure `GROQ_API_KEY` is properly defined in `.env`.
