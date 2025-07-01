# Django uchun Dockerfile

FROM python:3.11-slim


# Ishchi papkani o‘rnatish

WORKDIR /app


# Fayllarni nusxalash

COPY . /app


# Kerakli kutubxonalarni o‘rnatish

RUN pip install --upgrade pip && pip install -r requirements.txt


# Statik fayllarni tayyorlash (agar kerak bo‘lsa)
# Port ochish (optional)

EXPOSE 8000


# Container ishga tushganda Django serverni ishga tushiramiz

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

