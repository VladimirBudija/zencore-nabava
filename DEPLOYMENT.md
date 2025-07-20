# 🚀 Deployment Guide - Railway & GitHub

Ovaj vodič objašnjava kako deployati ZenCore sustav na Railway koristeći GitHub Actions.

## 📋 Preduvjeti

- GitHub račun s pretplatom
- Railway račun s pretplatom
- Kod pushan na GitHub repository

## 🔧 Postavljanje Railway

### 1. Kreiramje Railway projekta

1. Idite na [Railway.app](https://railway.app)
2. Kliknite "New Project"
3. Odaberite "Deploy from GitHub repo"
4. Odaberite vaš repository
5. Railway će automatski detektirati `railway.json` konfiguraciju

### 2. Postavljanje baze podataka

1. U Railway dashboardu kliknite "New Service"
2. Odaberite "Database" → "PostgreSQL"
3. Railway će automatski generirati `DATABASE_URL`

### 3. Postavljanje Redis-a

1. Kliknite "New Service"
2. Odaberite "Database" → "Redis"
3. Railway će automatski generirati `REDIS_URL`

### 4. Konfiguracija varijabli

U Railway dashboardu dodajte sljedeće environment varijable:

```bash
DATABASE_URL=postgresql://...  # Automatski generirano
REDIS_URL=redis://...          # Automatski generirano
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PORT=8000
```

## 🔑 GitHub Secrets

Dodajte sljedeće secrets u vaš GitHub repository:

1. Idite na repository → Settings → Secrets and variables → Actions
2. Dodajte:
   - `RAILWAY_TOKEN` - Railway API token
   - `RAILWAY_PROJECT_ID` - Railway project ID

### Kako dobiti Railway token:

1. Idite na Railway dashboard → Account → Tokens
2. Kliknite "New Token"
3. Kopirajte token u GitHub secret

### Kako dobiti Project ID:

1. U Railway dashboardu odaberite projekt
2. ID se nalazi u URL-u ili u Settings → General

## 🚀 Automatski Deployment

Nakon postavljanja, svaki push na `main` branch će automatski:

1. Pokrenuti testove
2. Deployati na Railway ako testovi prođu

## 📊 Monitoring

- **Railway Dashboard**: Pregled servisa, logova, metrika
- **GitHub Actions**: Pregled deployment statusa
- **Health Check**: `https://your-app.railway.app/health`

## 🔧 Ručni Deployment

```bash
# Instalacija Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

## 🛠️ Troubleshooting

### Česti problemi:

1. **Database connection error**
   - Provjerite `DATABASE_URL` u Railway varijablama
   - Provjerite je li PostgreSQL servis pokrenut

2. **Redis connection error**
   - Provjerite `REDIS_URL` u Railway varijablama
   - Provjerite je li Redis servis pokrenut

3. **Build error**
   - Provjerite `backend/Dockerfile`
   - Provjerite `requirements.txt`

### Logovi:

```bash
# Railway logovi
railway logs

# GitHub Actions logovi
# Idite na repository → Actions → Deploy to Railway
```

## 🌐 Custom Domain

1. U Railway dashboardu idite na Settings → Domains
2. Dodajte custom domain
3. Konfigurirajte DNS prema Railway uputama

## 📈 Scaling

Railway automatski skalira prema potrebi. Možete postaviti:
- Minimum instances
- Maximum instances
- CPU/Memory limits

## 💰 Troškovi

- Railway ima besplatni tier s ograničenjima
- Preporučujemo paid plan za produkciju
- Troškovi ovise o korištenju resursa 