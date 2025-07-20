# ZenCore - Sustav za materijalno knjigovodstvo

Kompletan sustav za praćenje materijala, usluga i regulatornih zahtjeva u prehrambenoj industriji.

## Komponente

- **Backend API**: FastAPI s CRUD operacijama za materijale i usluge
- **Baza podataka**: PostgreSQL s optimiziranim indeksima
- **Frontend**: Cursor App za upravljanje podacima
- **Batch taskovi**: Celery za automatske operacije
- **DevOps**: Docker Compose + GitHub Actions + Railway deployment

## Struktura projekta

```
├── backend/                 # FastAPI aplikacija
│   ├── app/
│   │   ├── models/         # SQLAlchemy modeli
│   │   ├── schemas/        # Pydantic sheme
│   │   ├── api/           # API endpointi
│   │   ├── core/          # Konfiguracija i auth
│   │   └── services/      # Business logika
│   ├── alembic/           # Migracije baze
│   └── requirements.txt
├── cursor-app/            # Cursor App konfiguracija
├── docker/               # Docker konfiguracija
├── .github/              # GitHub Actions
└── docker-compose.yml    # Lokalni razvoj
```

## 🚀 Pokretanje

### 🌐 Cloud Deployment (preporučeno)

Za deployment na Railway s GitHub Actions:

1. **Postavite Railway projekt** - vidi [DEPLOYMENT.md](DEPLOYMENT.md)
2. **Konfigurirajte GitHub Secrets**
3. **Push na main branch** - automatski deployment

### 💻 Lokalni razvoj

#### Brzo pokretanje (preporučeno)

```bash
# Pokreni sustav s jednom komandom
chmod +x start.sh
./start.sh
```

#### Ručno pokretanje

#### 1. Lokalni razvoj s Docker Compose

```bash
# Pokreni sve servise
docker-compose up -d

# Provjeri status servisa
docker-compose ps

# Pogledaj logove
docker-compose logs -f backend
```

#### 2. Inicijalizacija baze podataka

```bash
# Pokreni migracije
docker-compose exec backend alembic upgrade head

# Inicijaliziraj test podatke
docker-compose exec backend python init_db.py
```

### 3. Pristup aplikacijama

- **Backend API**: http://localhost:8000
- **API Dokumentacija**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 4. Test korisnici

Nakon inicijalizacije baze, dostupni su sljedeći korisnici:

- **Admin**: username: `admin`, password: `admin123`
- **User**: username: `user`, password: `user123`

## API Endpointi

### Autentikacija
- `POST /auth/token` - Login
- `POST /auth/register` - Registracija
- `GET /auth/me` - Trenutni korisnik

### Materijali i Usluge
- `GET /materials` - Lista materijala i usluga (s filtriranjem)
- `GET /materials/{id}` - Detalji materijala/usluge s kalkulacijama
- `POST /materials` - Novi materijal/usluga
- `PUT /materials/{id}` - Ažuriranje materijala/usluge
- `DELETE /materials/{id}` - Deaktivacija materijala/usluge

### Filtriranje i pretraživanje
- `GET /materials?item_type=materijal` - Samo materijali
- `GET /materials?item_type=usluga` - Samo usluge
- `GET /materials?category=adaptogen` - Po kategoriji
- `GET /materials?vendor_id=1` - Po dobavljaču
- `GET /materials?has_coa=true` - S COA certifikatom
- `GET /materials?search=ashwagandha` - Pretraživanje

### Statistike
- `GET /materials/statistics/summary` - Statistike materijala i usluga
- `GET /materials/categories/{category}/items` - Stavke po kategoriji
- `GET /materials/vendors/{vendor_id}/items` - Stavke po dobavljaču
- `GET /materials/regulatory/{status}/items` - Stavke po regulatornom statusu

### Kalkulacije (samo za materijale)
- `GET /materials/{id}/current-stock` - Trenutna zaliha
- `GET /materials/{id}/recommended-po` - Preporučena narudžba

### Dashboard
- `GET /dashboard/summary` - Rekapitulacija
- `GET /dashboard/stock-status` - Status zaliha
- `GET /dashboard/trends` - Trend utroška
- `GET /dashboard/recommendations` - Preporučene akcije

### Ostali entiteti
- `GET/POST/PUT/DELETE /vendors` - Dobavljači
- `GET/POST/PUT/DELETE /offers` - Ponude
- `GET/POST/PUT/DELETE /purchase-orders` - Narudžbe
- `GET/POST/PUT/DELETE /receipts` - Prijemi
- `GET/POST/PUT/DELETE /consumptions` - Utrošak

## Podržani tipovi stavki

### Materijali
- **Adaptogeni**: Ashwagandha, Rhodiola, itd.
- **Nootropici**: Kognitivni boosteri
- **Vitamini**: D3, B kompleks, itd.
- **Minerali**: Magnezij, cink, itd.
- **Fosfolipidi**: Lećitin, itd.
- **Arome**: Prirodni aromi
- **Pomoćne tvari**: Antiaglomeranti, konzervansi

### Usluge
- **Proizvodnja**: Kapsuliranje, tableti
- **Pakiranje**: Etiketiranje, pakiranje
- **Prijevoz**: Hladnjački prijevoz
- **Skladištenje**: Kontrolirano skladištenje
- **Marketing**: Promocija, distribucija

## Kalkulacije

Sustav automatski izračunava:

1. **Trenutna zaliha** = Početna zaliha + Suma prijema - Suma utroška (samo za materijale)
2. **Preporučena narudžba** = (Sigurnosna zaliha + Mjesečni forecast - Trenutna zaliha) × 1.2
3. **Status zaliha**:
   - `critical`: ≤ 50% sigurnosne zalihe
   - `low`: ≤ sigurnosne zalihe
   - `normal`: > sigurnosne zalihe

## Regulatorno praćenje

- **COA certifikati**: Praćenje certifikata analize
- **Regulatorni status**: Novel food, dodatak prehrani, itd.
- **Rok trajanja**: Praćenje isteka roka
- **Batch brojevi**: Praćenje serija
- **Analitičke metode**: HPLC, DLS, UV-Vis

## Batch Taskovi

Celery taskovi se pokreću automatski:

- **Noćna sync s ERP-om**: 02:00 svaki dan
- **Obavijesti o niskim zalihama**: 09:00 svaki dan
- **Dnevni izvještaj**: 18:00 svaki dan
- **Provjera zaliha**: Svaki sat

## Cursor App

Cursor App je konfiguriran za:
- Dashboard s rekapitulacijom
- Upravljanje materijalima s kalkulacijama
- CRUD operacije za sve entitete
- Automatsko prikazivanje podataka bez dodatnog koda

## Razvoj

### Dodavanje novih migracija

```bash
# Generiraj novu migraciju
docker-compose exec backend alembic revision --autogenerate -m "Opis promjene"

# Pokreni migracije
docker-compose exec backend alembic upgrade head
```

### Pokretanje Celery taskova

```bash
# Worker
docker-compose exec backend celery -A app.celery_app worker --loglevel=info

# Beat scheduler
docker-compose exec backend celery -A app.celery_app beat --loglevel=info
```

### Testiranje

```bash
# Testiraj API s test skriptom
python test_api.py

# Pokreni unit testove
docker-compose exec backend pytest

# S pokrivenošću
docker-compose exec backend pytest --cov=app
```

## Produkcija

### Environment varijable

Kreirajte `.env` datoteku s:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379
SECRET_KEY=your-secret-key
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### Deployment

1. Postavite Docker Hub credentials u GitHub Secrets
2. Push na `main` branch pokreće CI/CD pipeline
3. Automatski se builda i deploya Docker image

## Troubleshooting

### Baza podataka ne pokreće se
```bash
docker-compose down -v
docker-compose up -d postgres
# Pričekajte da se baza pokrene, zatim pokrenite ostale servise
```

### Celery taskovi ne rade
```bash
# Provjeri Redis konekciju
docker-compose exec redis redis-cli ping

# Restart Celery servisa
docker-compose restart celery-worker celery-beat
```

### API ne odgovara
```bash
# Provjeri logove
docker-compose logs backend

# Restart backend servisa
docker-compose restart backend
``` 