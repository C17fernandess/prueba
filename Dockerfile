FROM python:3.12-slim as build

WORKDIR /app

COPY requeriments.txt ./

RUN pip install -r requeriments.txt

COPY . .

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "port=8000"]