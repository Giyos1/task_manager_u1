# Django uchun Dockerfile
FROM python:3.11-slim

# Ishchi papkani o‘rnatish
WORKDIR /app

# Fayllarni nusxalash
COPY . /app

# Kerakli kutubxonalarni o‘rnatish
RUN pip install --upgrade pip && pip install -r requirment.txt

# Statik fayllarni tayyorlash (agar kerak bo‘lsa)
RUN python manage.py collectstatic

# Port ochish (optional)
EXPOSE 8000

