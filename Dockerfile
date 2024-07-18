FROM python:alpine3.20

WORKDIR /usr/src/app

COPY requeriments.txt .
RUN pip install -r requeriments.txt

COPY . .

RUN chmod +x pruebaTecnica.py

EXPOSE 5000

CMD [ "python3", "pruebaTecnica.py" ]

    