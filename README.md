# Traveler LLM

> AI-powered travel itinerary generation with feedback-driven quality improvement.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B.svg)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-API-f55036.svg)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED.svg)](https://www.docker.com/)

A modular travel-planning application that generates personalized itineraries from destination, duration, interests, budget, and travel style, while capturing user feedback and operational telemetry for continuous improvement.

## Overview
Traveler LLM is a modular AI travel-planning application that generates personalized itineraries from destination, trip duration, interests, budget, and travel style. It persists trips, itineraries, feedback, telemetry, and training-related data in PostgreSQL and uses a provider abstraction for LLM inference.

## Key Capabilities
- Personalized itinerary generation
- Configurable LLM provider integration
- Structured trip and itinerary persistence
- User ratings and qualitative feedback
- Event and generation telemetry
- Analytics and operational dashboards
- Training-data collection and queueing
- Docker-based local deployment

## How It Works
```mermaid
flowchart LR
    A[User Input] --> B[Planner Service]
    B --> C[Groq LLM]
    C --> D[Itinerary Generation]
    D --> E[User Feedback]
    E --> F[Learning Queue]
```
- Users provide destination, dates, and preferences via the Streamlit UI.
- The input is passed to the Planner Service, which constructs a prompt.
- The Groq provider handles LLM inference.
- Generated itineraries are stored in PostgreSQL.
- Users can rate the itineraries and provide feedback.
- Telemetry and feedback are captured and added to a training queue for background processing.

## Architecture
Traveler LLM follows a modular-monolith architecture with clear separation between presentation, application services, repositories, infrastructure, and LLM provider integrations.

```text
┌─────────────────────┐
│    Streamlit UI     │
├─────────────────────┤
│ Application Services│
├─────────────────────┤
│    Repositories     │
├─────────────────────┤
│   Infrastructure    │
├─────────────────────┤
│ PostgreSQL │ LLM API │
└─────────────────────┘
```

## Tech Stack
| Layer | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| Database | PostgreSQL 14 |
| Database Driver | psycopg2 |
| LLM Provider | Groq |
| Containerization | Docker / Docker Compose |
| Testing | pytest |
| CI | GitHub Actions |
| Configuration | Environment variables + database configuration |

## Project Structure
```text
traveler-llm/
├── src/
│   ├── domain/
│   ├── infrastructure/
│   ├── pipelines/
│   ├── providers/
│   ├── repositories/
│   ├── services/
│   └── ui/
├── docs/
├── migrations/
├── prompts/
├── scripts/
├── .github/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```
The source tree follows a layered modular architecture separating UI, application logic, domain models, persistence, and infrastructure concerns.

## Getting Started

### Prerequisites
- Python 3.10+
- Docker and Docker Compose
- Groq API key

### 1. Clone
```bash
git clone https://github.com/your-org/traveler-llm.git
cd traveler-llm
```

### 2. Configure environment
```bash
cp .env.example .env
```
Set in `.env`:
```ini
GROQ_API_KEY=gsk_your_api_key_here
```

### 3. Start dependencies
```bash
docker compose up -d
```

### 4. Initialize database
```bash
docker compose exec app python setup_database.py
```

### 5. Run application
The application is automatically started by Docker Compose. Open your browser to:
http://localhost:8501

## Configuration
| Variable | Required | Purpose |
|---|---:|---|
| `GROQ_API_KEY` | Yes | LLM provider authentication |
| `DATABASE_URL` | Yes | PostgreSQL connection |

*(Note: Additional configuration variables exist in the database schema but are not yet enforced by the application logic).*

## Continuous Feedback Pipeline
```text
User Feedback
      ↓
Feedback Persistence
      ↓
Training Data
      ↓
Dataset Construction
      ↓
Evaluation
      ↓
Model Promotion
```

| Stage | Status |
|---|---|
| Feedback collection | ✅ Implemented |
| Training-data queueing | ✅ Implemented |
| Dataset construction | ⚠️ In progress |
| Model evaluation | ⚠️ In progress |
| Model promotion | ⚠️ In progress |
| Automated model improvement | ⚠️ Not yet production-ready |

## Current Status
| Area | Status |
|---|---|
| Core itinerary generation | ✅ Functional |
| PostgreSQL persistence | ✅ Implemented |
| Feedback collection | ✅ Implemented |
| Telemetry | ✅ Implemented |
| Docker deployment | ⚠️ Requires remediation |
| Automated tests | ❌ Not yet implemented |
| Continuous learning pipeline | ⚠️ Partial |
| Authentication / RBAC | ⚠️ Not implemented |
| Production deployment | ❌ Not yet production-ready |

See the [Audit Report](AUDIT_REPORT.md) for more detailed technical status.

## Documentation
| Document | Purpose |
|---|---|
| [Architecture](docs/architecture.md) | System architecture and design decisions |
| [Deployment Guide](docs/deployment_guide.md) | Deployment and environment configuration |
| [Operations Guide](docs/operations_guide.md) | Operational procedures and troubleshooting |
| [Database Documentation](docs/database_schema.md) | Schema and persistence model |
| [Design System](docs/DESIGN_SYSTEM.md) | UI conventions and components |
| [ADRs](docs/adr/) | Architecture Decision Records |

## Security
- Never commit `.env` files or credentials.
- Store API keys and database credentials through environment/secret management.
- Do not expose administrative or database-management interfaces publicly.
- Treat LLM-generated content as untrusted data.
- Report security issues privately rather than opening a public issue containing sensitive details.

## Development
Format:
```bash
black src
```
Lint:
```bash
ruff check src
```

## License
This project is licensed under the MIT License.
See [LICENSE](LICENSE) for details.
