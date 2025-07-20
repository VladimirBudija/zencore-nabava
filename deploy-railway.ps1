Write-Host "🚀 Railway Deployment Script" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

# Provjeri je li Node.js instaliran
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js nije instaliran. Molim instalirajte Node.js s https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Provjeri je li Railway CLI instaliran
if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Instaliram Railway CLI..." -ForegroundColor Yellow
    npm install -g @railway/cli
}

# Provjeri je li korisnik logiran
try {
    railway whoami | Out-Null
    Write-Host "✅ Railway CLI je spreman" -ForegroundColor Green
} catch {
    Write-Host "🔑 Molim se prijavite na Railway..." -ForegroundColor Yellow
    railway login
}

# Deploy na Railway
Write-Host "🚀 Pokretanje deploymenta..." -ForegroundColor Green
railway up

Write-Host ""
Write-Host "🎉 Deployment završen!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Za pregled statusa:" -ForegroundColor Cyan
Write-Host "   railway status"
Write-Host ""
Write-Host "📋 Za pregled logova:" -ForegroundColor Cyan
Write-Host "   railway logs"
Write-Host ""
Write-Host "🌐 Za otvaranje aplikacije:" -ForegroundColor Cyan
Write-Host "   railway open" 