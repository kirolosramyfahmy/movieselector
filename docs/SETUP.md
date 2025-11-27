# 🎬 Movie Recommender - Guide de démarrage

## 📋 Prérequis

- **Node.js** 18+ ([télécharger](https://nodejs.org/))
- **Python** 3.11+ ([télécharger](https://www.python.org/downloads/))
- **PostgreSQL** 15+ ([télécharger](https://www.postgresql.org/download/))
- **Redis** 7+ ([télécharger](https://redis.io/download))
- **Compte TMDB API** (gratuit, [créer un compte](https://www.themoviedb.org/settings/api))

## 🚀 Installation

### 1. Cloner le projet

```bash
cd /Users/kiro37/Documents/fllmproject/movie-recommender
```

### 2. Configuration de l'environnement

Créez un fichier `.env` à la racine du projet :

```bash
cp .env.example .env
```

Éditez `.env` et ajoutez votre clé API TMDB :

```env
TMDB_API_KEY=votre_cle_api_tmdb_ici
```

### 3. Installation du Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux:
source venv/bin/activate
# Sur Windows:
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Installation du Frontend

```bash
cd ../frontend

# Installer les dépendances
npm install
```

### 5. Démarrer les services

#### Option A : Avec Docker (Recommandé)

```bash
# À la racine du projet
docker-compose up -d
```

#### Option B : Manuellement

**Terminal 1 - PostgreSQL** (si pas déjà installé comme service)
```bash
# Créer la base de données
createdb movie_recommender
```

**Terminal 2 - Redis**
```bash
redis-server
```

**Terminal 3 - Backend**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 4 - Frontend**
```bash
cd frontend
npm run dev
```

### 6. Peupler la base de données

```bash
cd backend
source venv/bin/activate
python scripts/populate_db.py
```

Ce script va :
- Récupérer ~1000 films depuis TMDB
- Calculer les similarités entre films
- Cela peut prendre 10-15 minutes

## 🌐 Accès à l'application

- **Frontend** : http://localhost:5173
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## 🎯 Utilisation

1. Ouvrez http://localhost:5173
2. Cliquez sur "Commencer"
3. Sélectionnez vos films préférés (recherche ou films populaires)
4. Consultez les films similaires suggérés automatiquement
5. Cliquez sur "Obtenir mes recommandations"
6. Affinez avec les boutons "J'aime" / "Je n'aime pas"
7. Partagez vos recommandations !

## 🛠️ Commandes utiles

### Backend

```bash
# Lancer les tests
pytest

# Créer une migration
alembic revision --autogenerate -m "description"

# Appliquer les migrations
alembic upgrade head

# Mettre à jour les films
python scripts/populate_db.py
```

### Frontend

```bash
# Développement
npm run dev

# Build production
npm run build

# Preview production
npm run preview
```

## 🐛 Dépannage

### Erreur de connexion à la base de données

Vérifiez que PostgreSQL est démarré et que les credentials dans `.env` sont corrects.

### Erreur TMDB API

Vérifiez que votre clé API TMDB est valide et correctement configurée dans `.env`.

### Port déjà utilisé

Si le port 5173 ou 8000 est déjà utilisé, modifiez-le dans :
- Frontend : `vite.config.js`
- Backend : lancez avec `uvicorn app.main:app --port 8001`

## 📚 Documentation

- [TMDB API Documentation](https://developers.themoviedb.org/3)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [GSAP Documentation](https://greensock.com/docs/)

## 🤝 Support

Pour toute question ou problème, consultez la documentation ou créez une issue.
