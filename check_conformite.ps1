# Script de Vérification de Conformité - DZ-Volunteer Backend
# Exécute tous les contrôles de qualité et affiche un rapport

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   🎯 VÉRIFICATION CONFORMITÉ CAHIER DES CHARGES" -ForegroundColor Cyan
Write-Host "   Projet: DZ-Volunteer Backend Django" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Compteurs
$total_checks = 0
$passed_checks = 0
$failed_checks = 0

# Fonction pour afficher le résultat d'un test
function Test-Item {
    param(
        [string]$Name,
        [scriptblock]$Check,
        [string]$SuccessMsg,
        [string]$FailMsg
    )
    
    $script:total_checks++
    Write-Host "Vérification: " -NoNewline
    Write-Host "$Name" -ForegroundColor Yellow -NoNewline
    Write-Host " ... " -NoNewline
    
    try {
        $result = & $Check
        if ($result) {
            Write-Host "✅ PASS" -ForegroundColor Green
            if ($SuccessMsg) { Write-Host "   → $SuccessMsg" -ForegroundColor Gray }
            $script:passed_checks++
            return $true
        } else {
            Write-Host "❌ FAIL" -ForegroundColor Red
            if ($FailMsg) { Write-Host "   → $FailMsg" -ForegroundColor Gray }
            $script:failed_checks++
            return $false
        }
    } catch {
        Write-Host "❌ ERROR" -ForegroundColor Red
        Write-Host "   → $($_.Exception.Message)" -ForegroundColor Gray
        $script:failed_checks++
        return $false
    }
}

# Vérifier qu'on est dans le bon répertoire
if (-not (Test-Path "backend")) {
    Write-Host "❌ Erreur: Ce script doit être exécuté depuis la racine du projet" -ForegroundColor Red
    exit 1
}

cd backend

Write-Host ""
Write-Host "📋 SECTION 1: FICHIERS ET STRUCTURE" -ForegroundColor Magenta
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Gray

Test-Item "Fichier requirements.txt" `
    { Test-Path "requirements.txt" } `
    "requirements.txt trouvé" `
    "requirements.txt manquant"

Test-Item "Fichier requirements-dev.txt" `
    { Test-Path "requirements-dev.txt" } `
    "requirements-dev.txt trouvé" `
    "requirements-dev.txt manquant"

Test-Item "Fichier .env" `
    { Test-Path ".env" } `
    ".env configuré" `
    ".env manquant - copier .env.example"

Test-Item "Dockerfile" `
    { Test-Path "Dockerfile" } `
    "Dockerfile trouvé" `
    "Dockerfile manquant"

Test-Item "docker-compose.yml" `
    { Test-Path "../docker-compose.yml" } `
    "docker-compose.yml trouvé" `
    "docker-compose.yml manquant"

Test-Item "Pipeline CI/CD" `
    { Test-Path "../.github/workflows/ci-cd.yml" } `
    "GitHub Actions configuré" `
    "Pipeline CI/CD manquant"

Write-Host ""
Write-Host "🧪 SECTION 2: TESTS" -ForegroundColor Magenta
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Gray

Test-Item "Dossier tests/" `
    { Test-Path "tests" } `
    "Structure tests/ créée" `
    "Créer le dossier tests/"

Test-Item "Tests unitaires" `
    { (Test-Path "tests/unit/test_volunteer_logic.py") -and (Test-Path "tests/unit/test_mission_logic.py") } `
    "Tests unitaires présents" `
    "Tests unitaires manquants"

Test-Item "Tests d'intégration" `
    { Test-Path "tests/integration/test_api.py" } `
    "Tests d'intégration présents" `
    "Tests d'intégration manquants"

Test-Item "Configuration pytest" `
    { Test-Path "pytest.ini" } `
    "pytest.ini configuré" `
    "pytest.ini manquant"

Test-Item "Configuration coverage" `
    { Test-Path ".coveragerc" } `
    ".coveragerc configuré" `
    ".coveragerc manquant"

Write-Host ""
Write-Host "⚙️ SECTION 3: QUALITÉ DU CODE" -ForegroundColor Magenta
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Gray

Test-Item "Configuration Black" `
    { Test-Path "pyproject.toml" } `
    "pyproject.toml trouvé" `
    "pyproject.toml manquant"

Test-Item "Configuration Flake8" `
    { Test-Path ".flake8" } `
    ".flake8 configuré" `
    ".flake8 manquant"

Test-Item "Fichier .gitignore" `
    { Test-Path ".gitignore" } `
    ".gitignore présent" `
    ".gitignore manquant"

Write-Host ""
Write-Host "📐 SECTION 4: DIAGRAMMES UML" -ForegroundColor Magenta
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Gray

Test-Item "Diagramme Cas d'Utilisation" `
    { Test-Path "docs/uml/use-case-diagram.puml" } `
    "use-case-diagram.puml trouvé" `
    "use-case-diagram.puml manquant"

Test-Item "Diagramme de Classes" `
    { Test-Path "docs/uml/class-diagram.puml" } `
    "class-diagram.puml trouvé" `
    "class-diagram.puml manquant"

Test-Item "Diagramme de Composants" `
    { Test-Path "docs/uml/component-diagram.puml" } `
    "component-diagram.puml trouvé" `
    "component-diagram.puml manquant"

Test-Item "Diagramme Séquence Application" `
    { Test-Path "docs/uml/sequence-application.puml" } `
    "sequence-application.puml trouvé" `
    "sequence-application.puml manquant"

Test-Item "Diagramme Séquence Validation" `
    { Test-Path "docs/uml/sequence-validation-hours.puml" } `
    "sequence-validation-hours.puml trouvé" `
    "sequence-validation-hours.puml manquant"

Write-Host ""
Write-Host "📚 SECTION 5: DOCUMENTATION" -ForegroundColor Magenta
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Gray

Test-Item "README.md" `
    { Test-Path "README.md" } `
    "README.md présent" `
    "README.md manquant"

Test-Item "API_GUIDE.md" `
    { Test-Path "API_GUIDE.md" } `
    "API_GUIDE.md présent" `
    "API_GUIDE.md manquant"

Test-Item "DATABASE_SETUP.md" `
    { Test-Path "DATABASE_SETUP.md" } `
    "DATABASE_SETUP.md présent" `
    "DATABASE_SETUP.md manquant"

Test-Item "QUICKSTART.md" `
    { Test-Path "QUICKSTART.md" } `
    "QUICKSTART.md présent" `
    "QUICKSTART.md manquant"

Test-Item "AUDIT_CONFORMITE.md" `
    { Test-Path "AUDIT_CONFORMITE.md" } `
    "AUDIT_CONFORMITE.md présent" `
    "AUDIT_CONFORMITE.md manquant"

Write-Host ""
Write-Host "🏗️ SECTION 6: ARCHITECTURE DJANGO" -ForegroundColor Magenta
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Gray

Test-Item "App accounts/" `
    { Test-Path "accounts/models.py" } `
    "App accounts configurée" `
    "App accounts manquante"

Test-Item "App missions/" `
    { Test-Path "missions/models.py" } `
    "App missions configurée" `
    "App missions manquante"

Test-Item "App skills/" `
    { Test-Path "skills/models.py" } `
    "App skills configurée" `
    "App skills manquante"

Test-Item "App odd/" `
    { Test-Path "odd/models.py" } `
    "App odd configurée" `
    "App odd manquante"

Test-Item "Management command init_data" `
    { Test-Path "accounts/management/commands/init_data.py" } `
    "Command init_data présente" `
    "Command init_data manquante"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   📊 RÉSULTATS DE L'AUDIT" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$percentage = [math]::Round(($passed_checks / $total_checks) * 100, 1)

Write-Host "Total de vérifications: " -NoNewline
Write-Host "$total_checks" -ForegroundColor White

Write-Host "Vérifications réussies: " -NoNewline
Write-Host "$passed_checks" -ForegroundColor Green

Write-Host "Vérifications échouées: " -NoNewline
Write-Host "$failed_checks" -ForegroundColor Red

Write-Host ""
Write-Host "Score de conformité: " -NoNewline

if ($percentage -ge 90) {
    Write-Host "$percentage%" -ForegroundColor Green -NoNewline
    Write-Host " ✅ EXCELLENT" -ForegroundColor Green
} elseif ($percentage -ge 75) {
    Write-Host "$percentage%" -ForegroundColor Yellow -NoNewline
    Write-Host " ⚠️ BON (quelques améliorations possibles)" -ForegroundColor Yellow
} elseif ($percentage -ge 50) {
    Write-Host "$percentage%" -ForegroundColor Red -NoNewline
    Write-Host " ❌ INSUFFISANT" -ForegroundColor Red
} else {
    Write-Host "$percentage%" -ForegroundColor Red -NoNewline
    Write-Host " ❌ CRITIQUE" -ForegroundColor Red
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan

# Recommandations
if ($failed_checks -gt 0) {
    Write-Host ""
    Write-Host "💡 RECOMMANDATIONS:" -ForegroundColor Yellow
    Write-Host ""
    
    if (-not (Test-Path ".env")) {
        Write-Host "   • Copier .env.example vers .env et configurer les variables" -ForegroundColor Gray
    }
    
    if (-not (Test-Path "tests")) {
        Write-Host "   • Créer la structure de tests (voir PLAN_ACTION.md)" -ForegroundColor Gray
    }
    
    if (-not (Test-Path "docs/uml/use-case-diagram.puml")) {
        Write-Host "   • Créer les diagrammes UML manquants" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "📖 Consulter PLAN_ACTION.md pour les instructions détaillées" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Pour plus d'informations:" -ForegroundColor Gray
Write-Host "   • Audit complet: backend/AUDIT_CONFORMITE.md" -ForegroundColor Gray
Write-Host "   • Plan d'action: backend/docs/PLAN_ACTION.md" -ForegroundColor Gray
Write-Host "   • Résumé: CONFORMITE_RESUME.md" -ForegroundColor Gray
Write-Host ""

cd ..

# Retourner un code de sortie basé sur le score
if ($percentage -ge 90) {
    exit 0
} else {
    exit 1
}
