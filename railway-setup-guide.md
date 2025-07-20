# 🚀 Railway Setup Guide - ZenCore

## Korak 1: GitHub Repository

1. **Instalirajte Git** (ako nije instaliran):
   - Preuzmite s: https://git-scm.com/
   - Instalirajte s default postavkama

2. **Kreirajte GitHub repository**:
   - Idite na https://github.com/
   - Kliknite "New repository"
   - Nazovite: `zencore-nabava`
   - Ostavite javnim
   - Ne inicijalizirajte s README

3. **Push kod na GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - ZenCore system"
   git branch -M main
   git remote add origin https://github.com/VAS_USERNAME/zencore-nabava.git
   git push -u origin main
   ```

## Korak 2: Railway Projekt

1. **Idite na Railway**: https://railway.app
2. **Kliknite "New Project"**
3. **Odaberite "Deploy from GitHub repo"**
4. **Povežite GitHub račun**
5. **Odaberite `zencore-nabava` repository**

## Korak 3: Dodajte bazu podataka

1. **U Railway dashboardu kliknite "New Service"**
2. **Odaberite "Database" → "PostgreSQL"**
3. **Railway će automatski generirati `DATABASE_URL`**

## Korak 4: Dodajte Redis

1. **Kliknite "New Service"**
2. **Odaberite "Database" → "Redis"**
3. **Railway će automatski generirati `REDIS_URL`**

## Korak 5: Konfigurirajte Environment varijable

U Railway dashboardu, odaberite backend servis i dodajte:

```bash
# Obavezne varijable
SECRET_KEY=your-super-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PORT=8000

# Opcionalne varijable
LOG_LEVEL=INFO
```

## Korak 6: Pokrenite migracije

1. **U Railway dashboardu idite na backend servis**
2. **Kliknite "Deployments"**
3. **Kliknite na najnoviji deployment**
4. **Idite na "Logs" tab**
5. **Provjerite da li se aplikacija pokrenula**

## Korak 7: Inicijalizirajte bazu

1. **U Railway dashboardu idite na backend servis**
2. **Kliknite "Variables" tab**
3. **Dodajte varijablu**: `INIT_DB=true`
4. **Deploy ponovno**

## Korak 8: Testirajte aplikaciju

1. **Kliknite na backend servis u Railway**
2. **Kopirajte URL** (npr. https://your-app.railway.app)
3. **Dodajte `/docs` na kraj URL-a**
4. **Testirajte API endpointove**

## Korak 9: GitHub Actions (opcionalno)

Za automatski deployment:

1. **U GitHub repository idite na Settings → Secrets**
2. **Dodajte `RAILWAY_TOKEN`** (iz Railway dashboarda)
3. **Dodajte `RAILWAY_PROJECT_ID`** (iz Railway URL-a)

## 🌐 Pristup aplikaciji

- **API**: https://your-app.railway.app
- **Dokumentacija**: https://your-app.railway.app/docs
- **ReDoc**: https://your-app.railway.app/redoc
- **Health check**: https://your-app.railway.app/health

## 👤 Test korisnici

Nakon inicijalizacije baze:
- **Admin**: username=admin, password=admin123
- **User**: username=user, password=user123

## 📊 Monitoring

- **Railway Dashboard**: Pregled servisa, logova, metrika
- **GitHub Actions**: Pregled deployment statusa
- **Logovi**: Real-time logovi u Railway dashboardu

## 🔧 Troubleshooting

### Aplikacija se ne pokreće
- Provjerite logove u Railway dashboardu
- Provjerite environment varijable
- Provjerite da li je `PORT` postavljen

### Baza podataka nije povezana
- Provjerite `DATABASE_URL` u Railway varijablama
- Provjerite da li je PostgreSQL servis pokrenut

### Redis nije povezan
- Provjerite `REDIS_URL` u Railway varijablama
- Provjerite da li je Redis servis pokrenut 