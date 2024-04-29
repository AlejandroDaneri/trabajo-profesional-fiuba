FROM python:3.10

WORKDIR /app

COPY backtester .

COPY lib /app/lib

RUN pip install -r requirements.txt

EXPOSE 5000

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]