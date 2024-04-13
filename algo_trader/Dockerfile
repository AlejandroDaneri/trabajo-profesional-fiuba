FROM python:3.10.2

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV BOT_TOKEN="6575277104:AAGLL8gGGT65SU_gIX5KBdkV47fLVbTO9mI"

EXPOSE 8000

CMD ["python3","-u", "main.py"]
