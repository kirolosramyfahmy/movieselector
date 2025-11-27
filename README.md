# 🎬 Movie Recommender

Site web de recommandation de films basé sur vos préférences, avec une interface premium et fluide.

## 🏗️ Architecture

- **Frontend**: Vue.js + GSAP (animations)
- **Backend**: FastAPI + Python
- **Database**: PostgreSQL
- **Cache**: Redis
- **Data Source**: TMDB API

## 📁 Structure du projet

```
movie-recommender/
├── frontend/          # Application Vue.js
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── models/    # Modèles SQLAlchemy
│   │   ├── routes/    # Endpoints API
│   │   ├── services/  # Logique métier
│   │   ├── core/      # Configuration
│   │   └── utils/     # Utilitaires
│   ├── tests/         # Tests unitaires
│   └── scripts/       # Scripts de maintenance
├── scripts/           # Scripts d'automatisation
└── docs/              # Documentation
```

## 🚀 Quick Start

### Prérequis

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Compte TMDB API (gratuit)

### Installation

```bash
# Cloner le repository
git clone <repo-url>
cd movie-recommender

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install

# Configuration
cp .env.example .env
# Éditer .env avec vos clés API
```

### Lancement

```bash
# Backend (terminal 1)
cd backend
uvicorn app.main:app --reload

# Frontend (terminal 2)
cd frontend
npm run dev
```

## 🎨 Fonctionnalités

- ✨ Interface one-page avec scroll fluide
- 🎯 Recommandations basées sur vos films préférés
- 🔍 Recherche avec autocomplete
- 🎭 Filtres par genre, année, popularité
- 💫 Animations GSAP premium
- 📱 Responsive mobile-first
- 🔄 Feedback dynamique sur les recommandations
- 🔗 Partage sur réseaux sociaux

## 📝 License

MIT
