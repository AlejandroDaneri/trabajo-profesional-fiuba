FROM python:3.10

WORKDIR /app

COPY backtester .

COPY lib /app/lib

ENV PYTHONUNBUFFERED=1

RUN pip install -r requirements.txt

EXPOSE 5000

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "app:app"]