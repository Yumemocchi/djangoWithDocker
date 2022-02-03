# récupère l'image python
FROM python:alpine3.15

LABEL maintainer="app.localhost"

# set des variables d'environnement python
# Empêche d'écrire des fichiers pyc sur le disque (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

COPY ./src/requirements_prod.txt /requirements.txt
COPY ./src /app
COPY ./settings_prod.py /app/settings.py
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

# On est pas obligé de mettre un environnemnet virtuel pour python
# mais c'est mieux si on veut être certain qu'il n'y ait pas de conflit de dépendances
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install wheel && \
    apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev linux-headers && \
    apk add zlib-dev jpeg-dev && \
    /py/bin/pip install -r /requirements.txt && \
    # pas de password et pas de répertoire home pour le user app
    adduser --disabled-password --no-create-home app && \
    # création des répertoires pour les fichiers statiques (css, js, images..)
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


# on veut que notre PATH corresponde à l'environnement virtuel que l'on vient de créer
ENV PATH="/scripts:/py/bin:$PATH"

# à partir de maintenant on utilise le user app et non root
USER app


CMD ["run.sh"]