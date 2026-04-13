# DeployHub — Dog Breed Explorer
Module: IS2209  
Group: 8  
Members: 4
| Name | Student Number |
|------|---------------|
| David Byrne | 124476136 |
| Darragh McEniry | 124467352 |
| David Harte | 124435506 |
| Luke Mulcahy | 124476112 |

**GitHub Repository:** https://github.com/DavidByrne1111/FlaskGP  
**Live Website:** https://flaskgp.onrender.com

---

## What it does
Dog Breed Explorer is a Flask web application that integrates two external services:
1. Dog CEO API — fetches a random dog photo for a selected breed
2. Supabase PostgreSQL — saves and retrieves previously fetched photos

Users can pick a breed, fetch a photo, and save it to the database. Recently saved photos appear at the bottom of the page.

---

## Setup & Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/DavidByrne1111/FlaskGP.git
cd FlaskGP
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy `.env.example` to `.env` and fill in your real values:
```bash
cp .env.example .env
```

Your `.env` should contain: DATABASE_URL=postgresql://user:password@host:5432/dbname

### 5. Run the app
```bash
python app.py
```

Visit http://localhost:5000 in your browser.

---

## Environment Variables
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string from Supabase |

---

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main UI page |
| `/api/dog/<breed>` | GET | Fetch random photo for a breed |
| `/api/save` | POST | Save a breed photo to the database |
| `/api/saved` | GET | Get 10 most recently saved photos |
| `/health` | GET | Health check — returns `{"status": "ok"}` |
| `/status` | GET | Diagnostics — DB and API connectivity |

---

## CI/CD Overview
- **CI:** GitHub Actions runs on every PR and push to master
  - Linting with `ruff`
  - Tests with `pytest` and coverage report
  - Docker image build
- **CD:** Automatically deploys to Render on every push to master
- **Container:** Dockerfile included for local containerised runs
- **Release:** Tagged as `v1.0.0` with changelog

---

## Running Tests
```bash
pip install pytest pytest-cov
pytest test_app.py -v --cov=app --cov-report=term-missing
```

---

## Running with Docker
```bash
docker build -t flaskgp .
docker run -e DATABASE_URL=your_url_here -p 5000:5000 flaskgp
```

---

## External Code & Citations
- [Dog CEO API](https://dog.ceo/dog-api/) — public dog image API
- [Supabase](https://supabase.com) — managed PostgreSQL database
- [Flask Documentation](https://flask.palletsprojects.com/)
- [psycopg2](https://www.psycopg.org/docs/)