#!/bin/bash
set -e

echo "⏳ PostgreSQL va Redis tayyor bo‘lguncha kutilyapti..."

# 1. PostgreSQL porti ochilishini kutish
while ! nc -z db 5432; do
  echo "⏳ PostgreSQL porti hali ochilmagan — kutilyapti..."
  sleep 1
done
echo "✅ PostgreSQL porti ochiq."

# 2. Redis porti ochilishini kutish
while ! nc -z redis 6379; do
  echo "⏳ Redis porti hali ochilmagan — kutilyapti..."
  sleep 1
done
echo "✅ Redis porti ochiq."

# 3. Statik fayllarni yig‘ish
echo "⚙️  Statik fayllar yig‘ilmoqda..."
python manage.py collectstatic --noinput


# 4. Migrationsni qo‘llash
echo "⚙️  Migratsiyalar qo‘llanmoqda..."
python manage.py migrate

# Skriptga argument sifatida berilgan buyruqni bajarish
# Bu "web", "celery", "celery-beat" xizmatlari uchun alohida buyruqlarni ishga tushirish imkonini beradi.
exec "$@"

