#!/bin/bash
set -e

echo "🚀 Starting ADHD Coach (Telegram-only)..."

# Fix Alembic heads (one-time fix for migration cleanup)
echo "🔧 Fixing Alembic migration heads..."
python3 fix_alembic_heads.py || echo "⚠️  Fix script failed or already fixed"

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head
echo "✅ Migrations complete"

# Start Telegram bot in foreground (no web server needed)
echo "📱 Starting Telegram bot..."
python3 run_telegram_bot.py
