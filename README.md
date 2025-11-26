# AI-Powered Job Portal (Resume Parser + Matching Engine)

A full-stack Django project that allows candidates to upload resumes, recruiters to post jobs, and an AI engine to match resumes with job descriptions using embeddings.

This project demonstrates backend engineering, database design, authentication, role-based access, file handling, AI integration, and practical workflows used in real hiring systems.

## 🚀 Features

### 👤 User Roles
- **Candidate:** Upload resumes, view matching jobs, apply.
- **Recruiter:** Post jobs, view matching candidates.
- **Admin:** Manage the entire platform through Django admin.

### 📄 Resume Upload & Parsing
- Upload PDF resumes
- Text extraction using **PyPDF2 / pdfplumber**
- Optional OCR for scanned PDFs
- Parse and clean extracted text

### 🤖 AI Job Matching Engine
- Embedding generation using **sentence-transformers**
- Cosine similarity ranking between resume & job embeddings
- Shows best-matched jobs for each candidate
- Shows best-matched candidates for each recruiter

### 🧠 Skill & Metadata Extraction (Optional)
- Auto-detect skills, experience level, location, keywords
- Use heuristics or spaCy NER for structured data

### 🔍 Job Search & Filters
- Keyword search
- Location filter
- Experience filter
- Tag/Skill filter

### 📬 Email Notifications
- Resume upload confirmation
- New job match alerts
- Application status updates

### 🖥️ Dashboards
- Candidate Dashboard
- Recruiter Dashboard
- Admin Dashboard (Django default)

## 🏗️ Tech Stack

| Layer | Tools |
|------|--------|
| Backend | Django (no DRF initially) |
| Database | MySQL |
| AI/ML | Sentence Transformers |
| PDF Parsing | PyPDF2, pdfplumber |
| Frontend | Django Templates + HTML/CSS |
| Background Tasks (Optional) | Celery + Redis |
| Deployment | Docker / Render / Railway |

## 📂 Project Structure

```
jobportal/
    jobportal/        # settings, config
    users/            # auth, roles, profiles
    jobs/             # job posting, filtering
    matching/         # AI matching engine
    resumes/          # upload & parsing logic
    templates/        # HTML templates
    static/           # CSS, JS
```

## ⚙️ How It Works

### 1. Resume Uploaded
Candidate uploads PDF → system extracts text → embedding is generated → stored in DB.

### 2. Job Posted
Recruiter posts job → job description text processed → embedding generated.

### 3. Matching Engine
Cosine similarity = match score.  
Sorted list shown to candidates and recruiters.

## 📌 Installation

### 1. Clone the repo
```
git clone https://github.com/yourusername/ai-job-portal.git
cd ai-job-portal
```

### 2. Create virtual environment
```
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Setup MySQL database
Create a DB:
```
CREATE DATABASE jobportal;
```

Update `settings.py` with your MySQL credentials.

### 5. Run migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 6. Start development server
```
python manage.py runserver
```

## 🤖 AI Matching Engine Setup

Install sentence-transformers:
```
pip install sentence-transformers
```

Example embedding generation:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
vector = model.encode(text).tolist()
```

## 🔮 Future Enhancements
- DRF API layer
- Vector database (FAISS / Milvus / pgvector)
- Resume scoring explanation
- Multi-language resume parsing
- React-based frontend

## 🧑‍💻 Author
**Rohit**
Backend Engineer | Python | Django | AI | Automation
