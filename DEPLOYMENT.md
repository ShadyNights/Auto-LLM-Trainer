# Production Deployment Guide (Streamlit Community Cloud)

> [!NOTE]
> This guide outlines how to deploy Traveler LLM to production for free using **Streamlit Community Cloud** for the frontend, combined with a managed PostgreSQL provider (e.g., Neon or Supabase).

---

## 1. Database Infrastructure

Streamlit Community Cloud provides application hosting, but it does **not** host databases. You must provision a managed PostgreSQL database.

### Step 1: Provision PostgreSQL
1. Create a free account on [Neon.tech](https://neon.tech/) or [Supabase](https://supabase.com/).
2. Create a new PostgreSQL 14+ database instance.
3. Retrieve your **Connection URI** (e.g., `postgresql://user:password@hostname:5432/dbname`).

### Step 2: Initialize the Production Database
Before deploying the UI, you must initialize the unified schema in your production database. From your local machine:
1. Temporarily update your local `.env` file with the production database credentials.
2. Run the initialization script to establish the schema in the cloud:
   ```bash
   python setup_database.py
   ```
3. *(Optional)* Revert your local `.env` file back to your local database credentials.

---

## 2. Deploying the Streamlit UI

We will deploy the main application (`app.py`) via GitHub directly to Streamlit.

### Step 1: Prepare the Repository
Ensure all code (including `requirements.txt`) is committed and pushed to a public or private GitHub repository. 

### Step 2: Deploy to Streamlit Cloud
1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/) using your GitHub account.
2. Click **"New app"**.
3. Select your GitHub repository, branch (e.g., `main`), and set the **Main file path** to `app.py`.
4. Do **not** click Deploy yet.

### Step 3: Configure Production Secrets
Streamlit Cloud does not use `.env` files. Instead, it uses a secure secrets manager.
1. Click **"Advanced settings"** before deploying.
2. In the **Secrets** text box, format your environment variables exactly like a TOML file. Map your PostgreSQL variables appropriately:

```toml
GROQ_API_KEY = "gsk_your_production_key"
DB_HOST = "ep-cool-cloud-1234.us-east-2.aws.neon.tech"
DB_NAME = "traveler_db"
DB_USER = "traveler_app_user"
DB_PASSWORD = "production_secure_password"
DB_PORT = "5432"
```

3. Click **Save** and then click **Deploy!**

> [!TIP]
> The Streamlit app will now provision its container, install dependencies from `requirements.txt`, and securely connect to your cloud database.

---

## 3. Handling Background Jobs (The Learning Pipeline)

> [!WARNING]
> Streamlit Community Cloud is designed specifically to run the `app.py` web server. It **cannot** run persistent background workers or Cron jobs.

Because Traveler LLM utilizes a Continuous Feedback Learning Pipeline (`background_jobs.py`), you must execute these jobs outside of Streamlit to process user ratings and queues.

### Option A: GitHub Actions (Recommended / Free)
You can schedule the pipeline to run periodically using a GitHub Actions Cron workflow.

1. Create `.github/workflows/pipeline.yml`:
```yaml
name: Learning Pipeline
on:
  schedule:
    - cron: "0 * * * *" # Runs every hour
  workflow_dispatch: # Allows manual trigger

jobs:
  run-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - name: Execute Pipeline
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          DB_HOST: ${{ secrets.DB_HOST }}
          DB_NAME: ${{ secrets.DB_NAME }}
          DB_USER: ${{ secrets.DB_USER }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
          DB_PORT: "5432"
        run: python background_jobs.py pipeline
```
2. Add your secrets to your GitHub Repository Settings (Settings > Secrets and variables > Actions).

### Option B: Render or VPS (Continuous)
If you prefer a persistent worker rather than a scheduled cron job, you can deploy `background_jobs.py` to a cheap VPS (DigitalOcean Droplet, AWS EC2) or a PaaS like Render as a background worker process.

```bash
# Setup command for a VPS
crontab -e
# Add the following line to run every 15 minutes
*/15 * * * * cd /path/to/app && /path/to/venv/bin/python background_jobs.py pipeline >> /var/log/traveler_pipeline.log 2>&1
```
