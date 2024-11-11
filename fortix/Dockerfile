# Utiliser une image Python officielle
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# UPGRADING PIP
RUN pip install --upgrade pip pipenv gunicorn

# Copier le reste de l'application
COPY . .



# Exposer le port pour Django
# EXPOSE 8000

ENTRYPOINT [ "sh","./entrypoint.sh" ]

# Démarrer l'application Django après avoir attendu que MySQL soit prêt
# CMD ["/bin/bash", "-c", "python manage.py runserver 0.0.0.0:8000"]
