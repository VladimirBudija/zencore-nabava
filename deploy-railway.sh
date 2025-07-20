#!/bin/bash

echo "🚀 Railway Deployment Script"
echo "============================"

# Provjeri je li Railway CLI instaliran
if ! command -v railway &> /dev/null; then
    echo "📦 Instaliram Railway CLI..."
    npm install -g @railway/cli
fi

# Provjeri je li korisnik logiran
if ! railway whoami &> /dev/null; then
    echo "🔑 Molim se prijavite na Railway..."
    railway login
fi

echo "✅ Railway CLI je spreman"

# Deploy na Railway
echo "🚀 Pokretanje deploymenta..."
railway up

echo ""
echo "🎉 Deployment završen!"
echo ""
echo "📊 Za pregled statusa:"
echo "   railway status"
echo ""
echo "📋 Za pregled logova:"
echo "   railway logs"
echo ""
echo "🌐 Za otvaranje aplikacije:"
echo "   railway open" 