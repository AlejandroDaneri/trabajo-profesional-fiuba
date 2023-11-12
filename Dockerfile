FROM python:3.10.2
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
