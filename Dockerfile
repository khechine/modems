# Utilisez une image de base appropriée pour Python et Django
FROM python:3.9

# Définissez le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copiez les fichiers de votre projet Django dans le conteneur
COPY . /app

# Installez les dépendances de votre projet Django
RUN pip install -r requirements.txt

# Exposez le port sur lequel votre application écoute (par exemple, le port 8000 pour Django)
EXPOSE 8000

# Démarrez votre application Django lorsque le conteneur est lancé
CMD python manage.py runserver 0.0.0.0:8000