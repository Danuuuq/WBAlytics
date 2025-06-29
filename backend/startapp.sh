#!/bin/sh
set -e

echo "⏳ Ожидаем доступность базы данных на $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "🕐 База данных пока недоступна — ждем..."
  sleep 3
done
echo "✅ База данных доступна!"

echo "📦 Применяем миграции..."
python manage.py migrate

echo "📥 Загружаем категории..."
python manage.py load_categories

echo "🚀 Запускаем сервер..."
exec gunicorn --bind 0.0.0.0:8000 product_analytics.wsgi
