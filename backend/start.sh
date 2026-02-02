#!/bin/bash
set -e

echo "🚀 Starting ADHD Coach services..."

# Fix Alembic heads (one-time fix for migration cleanup)
echo "🔧 Fixing Alembic migration heads..."
python3 fix_alembic_heads.py || echo "⚠️  Fix script failed or already fixed"

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head
echo "✅ Migrations complete"

# Start Telegram bot in background
echo "📱 Starting Telegram bot..."
python3 run_telegram_bot.py &
TELEGRAM_PID=$!
echo "✅ Telegram bot started (PID: $TELEGRAM_PID)"

# Start web server in foreground
echo "🌐 Starting web server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
