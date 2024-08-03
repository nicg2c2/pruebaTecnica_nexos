FROM python:alpine3.20

USER root

# Actualizar e instalar dependencias básicas
RUN apk update && apk add --no-cache \
    bash \
    curl \
    git \
    && apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --upgrade pip \
    && apk del .build-deps

WORKDIR /usr/src/app

COPY requirements.txt AppTecnica.py ./  

RUN pip install -r requirements.txt && \
    chmod +x AppTecnica.py

EXPOSE 5000

CMD [ "python3", "AppTecnica.py" ]

    