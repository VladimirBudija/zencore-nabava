# Railway Environment Variables

Ove varijable trebate postaviti u Railway dashboardu:

## Obavezne varijable

```bash
# Database (automatski generirano kada dodate PostgreSQL servis)
DATABASE_URL=postgresql://username:password@host:port/database

# Redis (automatski generirano kada dodate Redis servis)
REDIS_URL=redis://username:password@host:port

# JWT Configuration
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Railway specific
PORT=8000
```

## Opcionalne varijable

```bash
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Slack Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

# Logging
LOG_LEVEL=INFO
```

## Kako postaviti u Railway:

1. Idite na Railway dashboard
2. Odaberite vaš projekt
3. Kliknite na servis (backend)
4. Idite na "Variables" tab
5. Dodajte svaku varijablu

## Sigurnosni savjeti:

- **SECRET_KEY**: Koristite jaku, slučajnu lozinku (min. 32 znaka)
- **DATABASE_URL**: Railway automatski generira siguran URL
- **REDIS_URL**: Railway automatski generira siguran URL
- Nikad ne commitajte stvarne vrijednosti u kod 