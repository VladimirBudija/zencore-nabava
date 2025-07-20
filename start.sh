#!/bin/bash

echo "🚀 Pokretanje ZenCore sustava..."
echo "=================================="

# Provjeri je li Docker dostupan
if ! command -v docker &> /dev/null; then
    echo "❌ Docker nije instaliran ili nije dostupan"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose nije instaliran ili nije dostupan"
    exit 1
fi

echo "✅ Docker i Docker Compose su dostupni"

# Zaustavi postojeće kontejnere ako postoje
echo "🛑 Zaustavljanje postojećih kontejnera..."
docker-compose down

# Pokreni sve servise
echo "🔧 Pokretanje servisa..."
docker-compose up -d

# Pričekaj da se baza podataka pokrene
echo "⏳ Čekam da se baza podataka pokrene..."
sleep 10

# Provjeri status servisa
echo "📊 Status servisa:"
docker-compose ps

# Pokreni migracije
echo "🗄️ Pokretanje migracija..."
docker-compose exec -T backend alembic upgrade head

# Inicijaliziraj test podatke
echo "📝 Inicijalizacija test podataka..."
docker-compose exec -T backend python init_db.py

echo ""
echo "🎉 ZenCore sustav je pokrenut!"
echo ""
echo "📱 Pristup aplikacijama:"
echo "   • Backend API: http://localhost:8000"
echo "   • API Dokumentacija: http://localhost:8000/docs"
echo "   • ReDoc: http://localhost:8000/redoc"
echo ""
echo "👤 Test korisnici:"
echo "   • Admin: username=admin, password=admin123"
echo "   • User: username=user, password=user123"
echo ""
echo "🧪 Za testiranje API-ja pokrenite:"
echo "   python test_api.py"
echo ""
echo "📋 Za pregled logova:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Za zaustavljanje:"
echo "   docker-compose down" 