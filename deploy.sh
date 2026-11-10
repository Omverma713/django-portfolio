#!/usr/bin/env bash
# deploy.sh — Run this on the EC2 server to update the portfolio
set -e

echo "📦 Pulling latest code from GitHub..."
cd /home/ubuntu/portfolio
git pull origin main

echo "🐍 Activating virtual environment..."
source venv/bin/activate

echo "📚 Installing/updating dependencies..."
pip install -r requirements.txt

echo "🗃️ Running migrations..."
python manage.py migrate --no-input

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🔄 Restarting Gunicorn..."
sudo systemctl restart portfolio

echo "✅ Deployment complete!"
