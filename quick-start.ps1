Write-Host "🚀 ZenCore Quick Start - Railway + GitHub" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Preduvjeti:" -ForegroundColor Yellow
Write-Host "1. Git instaliran (https://git-scm.com/)" -ForegroundColor White
Write-Host "2. GitHub račun" -ForegroundColor White
Write-Host "3. Railway račun (https://railway.app)" -ForegroundColor White
Write-Host ""

# Provjeri je li Git instaliran
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git nije instaliran!" -ForegroundColor Red
    Write-Host "Molim instalirajte Git s: https://git-scm.com/" -ForegroundColor Yellow
    Write-Host "Zatim restartajte PowerShell i pokrenite ovu skriptu ponovno." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git je instaliran" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 Koraci za deployment:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Kreirajte GitHub repository:" -ForegroundColor White
Write-Host "   - Idite na https://github.com/" -ForegroundColor Gray
Write-Host "   - Kliknite 'New repository'" -ForegroundColor Gray
Write-Host "   - Nazovite: zencore-nabava" -ForegroundColor Gray
Write-Host "   - Ostavite javnim" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Push kod na GitHub:" -ForegroundColor White
Write-Host "   git init" -ForegroundColor Gray
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Initial commit - ZenCore system'" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git remote add origin https://github.com/VAS_USERNAME/zencore-nabava.git" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Deploy na Railway:" -ForegroundColor White
Write-Host "   - Idite na https://railway.app" -ForegroundColor Gray
Write-Host "   - Kliknite 'New Project'" -ForegroundColor Gray
Write-Host "   - Odaberite 'Deploy from GitHub repo'" -ForegroundColor Gray
Write-Host "   - Odaberite vaš repository" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Dodajte bazu podataka:" -ForegroundColor White
Write-Host "   - Kliknite 'New Service' → 'Database' → 'PostgreSQL'" -ForegroundColor Gray
Write-Host "   - Kliknite 'New Service' → 'Database' → 'Redis'" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Konfigurirajte varijable:" -ForegroundColor White
Write-Host "   - U backend servisu dodajte:" -ForegroundColor Gray
Write-Host "     SECRET_KEY=your-super-secret-key-here" -ForegroundColor Gray
Write-Host "     ALGORITHM=HS256" -ForegroundColor Gray
Write-Host "     ACCESS_TOKEN_EXPIRE_MINUTES=30" -ForegroundColor Gray
Write-Host "     PORT=8000" -ForegroundColor Gray
Write-Host "     INIT_DB=true" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Testirajte aplikaciju:" -ForegroundColor White
Write-Host "   - Kliknite na backend servis" -ForegroundColor Gray
Write-Host "   - Kopirajte URL i dodajte /docs" -ForegroundColor Gray
Write-Host ""

Write-Host "📖 Detaljni vodič: railway-setup-guide.md" -ForegroundColor Cyan
Write-Host "📚 Dokumentacija: DEPLOYMENT.md" -ForegroundColor Cyan

Write-Host ""
Write-Host "🎯 Nakon deploymenta:" -ForegroundColor Green
Write-Host "- API: https://your-app.railway.app" -ForegroundColor White
Write-Host "- Dokumentacija: https://your-app.railway.app/docs" -ForegroundColor White
Write-Host "- Test korisnici: admin/admin123, user/user123" -ForegroundColor White 