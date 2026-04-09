# Quick Setup Script for Restaurant Management API

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Restaurant Management API - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Check PostgreSQL connection
Write-Host "Checking PostgreSQL setup..." -ForegroundColor Yellow
Write-Host "Please ensure PostgreSQL is running and database 'restaurant_db' exists" -ForegroundColor Yellow
Write-Host ""

$continue = Read-Host "Have you created the PostgreSQL database 'restaurant_db'? (y/n)"
if ($continue -ne 'y') {
    Write-Host ""
    Write-Host "Please create the database first:" -ForegroundColor Red
    Write-Host "  psql -U postgres" -ForegroundColor Yellow
    Write-Host "  CREATE DATABASE restaurant_db;" -ForegroundColor Yellow
    Write-Host ""
    exit
}

# Update .env if needed
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path .env) {
    Write-Host "✓ .env file found" -ForegroundColor Green
    Write-Host "Please verify your DATABASE_URL in .env file" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "✗ .env file not found!" -ForegroundColor Red
    exit
}

# Seed database
Write-Host "Initializing database with seed data..." -ForegroundColor Yellow
python seed.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Setup Complete! 🎉" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Test Credentials:" -ForegroundColor Yellow
    Write-Host "  Customer: customer@test.com / 123456" -ForegroundColor White
    Write-Host "  Owner: owner@test.com / 123456" -ForegroundColor White
    Write-Host ""
    Write-Host "Start the server with:" -ForegroundColor Yellow
    Write-Host "  python main.py" -ForegroundColor White
    Write-Host ""
    Write-Host "API Documentation:" -ForegroundColor Yellow
    Write-Host "  http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Setup failed! Please check the error messages above." -ForegroundColor Red
    Write-Host ""
}
